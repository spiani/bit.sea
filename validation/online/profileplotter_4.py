import argparse

def argument():
    parser = argparse.ArgumentParser(description = '''
    Plots profile images from NetCDF  files
    The schema is : Float vs Forecast, Analysis
    '''
    ,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(   '--previous_dir','-p ',
                                type = str,
                                required = True,
                                help = 'directory of previous chain, having both analysis and forecast')
    parser.add_argument(   '--actual_dir','-a',
                                type = str,
                                required = True,
                                help = 'directory of actual chain, having only analysis')
    parser.add_argument(   '--outdir','-o',
                                type = str,
                                required = True,
                                help = 'directory of output files')
    parser.add_argument(   '--xmlfile','-f',
                                type = str,
                                required = True,
                                help = 'output xml file for medeaf website')
    
    
 
    return parser.parse_args()
 
args = argument()

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as pl
import numpy as np
import matplotlib.patches as mpatches
import scipy.io as NC
from layer_integral import coastline
import glob,os
import datetime
#from instruments import superfloat as bio_float
from basins.region import Rectangle
from commons.time_interval import TimeInterval
from commons.utils import addsep
from datetime import timedelta
from instruments import float_ppcon as ppcon_float
import sys

VARLIST           = ['P_l','O2o','N3n','votemper','vosaline','PAR','POC',"P_c", "pH"]


def figure_generator(p):
    ''' Generates a figure to plot the matchups related to a bioFloat cycle
    There are 6 axes: map, temperature, salinity, chl, oxygen and nitrate

    Arguments:
    * p * is a profile object

    Returns
    fig, axes (array of axes handlers)
    '''
    fig, axs = pl.subplots(2,5, facecolor='w', edgecolor='k')
    hsize=16
    vsize=12
    fig.set_size_inches(hsize,vsize)
    #figtitle = " date="+p.time.strftime('%Y/%m/%d')+" float="+p.name()
    #fig.set_title(figtitle)
    fig.subplots_adjust(hspace = 0.15, wspace=0.3)
    axs = axs.ravel()

    ax = axs[0]
    c_lon, c_lat=coastline.get()
    ax.plot(c_lon,c_lat, color='#000000',linewidth=0.5)
    ax.plot(p.lon,p.lat,'ro')
    ax.set_xticks(np.arange(-6,36,2))
    ax.set_yticks(np.arange(0,100,2))
    ax.set_xlabel("lon")
    ax.set_ylabel("lat")
    ax.set_title(p.time.strftime('%Y/%m/%d'))
    extent=10 #degrees
    ax.set_xlim([p.lon -extent/2, p.lon+extent/2])
    ax.set_ylim([p.lat -extent/2, p.lat+extent/2])
    bbox=ax.get_position()

    deltax, _ =bbox.size
    new_deltay = deltax* hsize/vsize
    bottom = bbox.ymax - new_deltay
    ax.set_position([bbox.xmin, bottom, deltax, new_deltay])

    floatlabel = 'Float \n'+ p.name() +" - "+str(p._my_float.cycle)
    f_patch = mpatches.Patch(color=COLOR_LIST[0] , label='Model_forecast')
    b_patch = mpatches.Patch(color=COLOR_LIST[1] , label='Model_analysis')
    g_patch = mpatches.Patch(color=COLOR_LIST[2]  , label=floatlabel)

    if  ('B' in p.profile_flags) or ('P' in p.profile_flags):
         y_patch = mpatches.Patch(color=COLOR_LIST[-1], label='recFloat')
         ax.legend(handles=[f_patch, b_patch,g_patch, y_patch ], bbox_to_anchor=(0, -0.5), loc=2)
    else:
         ax.legend(handles=[f_patch, b_patch,g_patch], bbox_to_anchor=(0, -0.5), loc=2)
    for ax in axs[1:]:
        ax.set_ylim(0,400)
        ax.locator_params(axis='x',nbins=4)
        ax.yaxis.grid()

    for ax in [axs[2], axs[3], axs[4], axs[6], axs[7], axs[8], axs[9]]:
        ax.set_yticklabels([])

    return fig,axs


def bellacicco_conversion(Profile, Pres):
    ii=(Pres >= 400) & (Pres <= 500)
    POC = Profile *  52779.37 - 3.57 # Bellacicco 2019
    if ii.sum() > 0 :
       shift=POC[ii].mean()
       print( "POC: adding a shift of " + str(shift))
       Profile = POC - shift
       ii=Profile<=0
       Profile[ii] = 0.0
    return Profile

def ncreader(filename):
    ''' 
    returns 
    FLOAT, numpy array
    MODEL, numpy array
    time, datetime object
    Lon, numpy array with 1 value
    Lat numpy array with 1 value
    '''
    dtype=[(var,np.float32) for var in VARLIST]
    MODEL = np.zeros((101,),dtype=dtype)
    FLOAT = np.zeros((101,),dtype=dtype)

    f = NC.netcdf_file(filename, 'r')
    Lon= f.variables['longitude'].data.copy()
    Lat= f.variables['latitude'].data.copy()
    time = datetime.datetime.strptime(f.time.decode(),"%Y%m%d-%H:%M:%S")
    for var in VARLIST:
        A= f.variables[var + "_model"].data.copy()
        A[A > 1.e+19] =np.nan
        MODEL[var] = A 
        A= f.variables[var + "_float"].data.copy()
        A[A > 1.e+19] =np.nan
        FLOAT[var] = A 
    f.close()
    
    return FLOAT, MODEL, time, Lon, Lat


def getprofile(time,lon,lat):
    lon = float(lon)
    lat = float(lat)
    eps=0.001
    R=Rectangle(lon-eps,lon+eps,lat-eps,lat+eps)
    d=timedelta(minutes=30)
    Profilelist=ppcon_float.FloatSelector(None,TimeInterval.fromdatetimes(time-d, time+d),R)
    print(Profilelist )
    profile=Profilelist[0]
    return profile

def dump_xml(filexml):
    S=[]
    for filename in analysis_forecast_basenames:
        date=filename[:8]
        if not date in S: S.append(date)
    
    LINES=[]
    LINES.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    LINES.append("<root>\n")
    
    for date in S:
        LINES.append("<date day=\"" + date + "\">\n")
        for filename in analysis_forecast_basenames:
            if filename[:8] == date:
                LINES.append("<float wmo=\"" + filename[9:-3] + "\"></float>\n")
        LINES.append("</date>\n")
    LINES.append("</root>\n")

    fid=open(filexml,'w')
    fid.writelines(LINES)
    fid.close()

PREVIOUS_DIR= addsep(args.previous_dir) #"/pico/home/usera07ogs/a07ogs00/OPA/V2C-dev/wrkdir/2/POSTPROC/AVE_FREQ_1/online_validation/PREVIOUS/matchup_outputs/"
ACTUAL_DIR  = addsep(args.actual_dir)  #"/pico/home/usera07ogs/a07ogs00/OPA/V2C-dev/wrkdir/2/POSTPROC/AVE_FREQ_1/online_validation/ACTUAL/matchup_outputs/"
OUTDIR      = addsep(args.outdir)
xmlfile     = args.xmlfile

ANALYSIS_FORECAST_LIST = glob.glob(PREVIOUS_DIR + "*nc")
ONLY_ANALYSIS_LIST     = glob.glob(ACTUAL_DIR   + "*nc")
COLOR_LIST = ['g','b','r','orange']

analysis_forecast_basenames = [os.path.basename(filename) for filename in ANALYSIS_FORECAST_LIST]
analysis_forecast_basenames.sort()
only_analyis_basenames      = [os.path.basename(filename) for filename in ONLY_ANALYSIS_LIST]
only_analyis_basenames.sort()

dump_xml(xmlfile)

zlevels_out=np.arange(0,501,5)
mapgraph = [5,3,7,1,2,4,8,6,9]

plotvarname = [r'Chl  $[ mg/m^3]$',
               r'Oxy  $[ mmol/m^3]$',
               r'Nitr $[ mmol/m^3]$',
               r'Temp $[ ^\circ C]$',
               'Sal [psu]',
               r'PAR  $[ \mu E/m^2 s]$',
               r'POC  $[ mg/m^3]$',
               'PhytoC $[ mg/m^3]$',
               'pH'
                ]

VARLIST           = ['P_l','O2o','N3n','votemper','vosaline','PAR','POC',"P_c", "pH"]
PPCON_VARLIST_mod = ['P_l','N3n','POC']
VARLIST_obs       = ['CHLA','NITRATE','BBP700']


for filename in analysis_forecast_basenames:
    if filename in only_analyis_basenames:
        print (filename, " matches analysis and forecast")
        analyis_file = ACTUAL_DIR + filename
        forecastfile = PREVIOUS_DIR + filename
        float_f, mod_f, time, lon, lat = ncreader(forecastfile)
        float_a, mod_a, time, lon, lat = ncreader(analyis_file) # float_f and float_f are identical
        p = getprofile(time, lon, lat) # p belong to ppcon_floar
        fig, axs = figure_generator(p)
        for i,var in enumerate(VARLIST):
            ax=axs[mapgraph[i]]
            if var in PPCON_VARLIST_mod: #['P_l','N3n','POC']

               var_idx = PPCON_VARLIST_mod.index(var)
               var_fl  = VARLIST_obs[var_idx]
               var_flpp= var_fl+'_PPCON'
               LIST_AVA_PARA =  list(p.available_params.split(" "))

               #181 COLOR_LIST = ['g','b','r','orange']               
               if (var_fl in LIST_AVA_PARA ) : # if es NITRATE in avail.params
                   if var_fl =='BBP700':
                      float_var = bellacicco_conversion(float_f[var],zlevels_out ) 
                   else:
                      float_var = float_f[var] 

                   if p._my_float.status_profile(var_fl) == 'P':
                       if var_fl in ['CHLA', 'BBP700', 'POC']: #ppcon plotted as 0-200m profile
                           ax.plot(float_var[zlevels_out<=200],zlevels_out[zlevels_out<=200], COLOR_LIST[-1])
                       else: 
                           ax.plot(float_var,zlevels_out, COLOR_LIST[-1])    

                   elif p._my_float.status_profile(var_fl) =='B': # insitu  and  ppcon
                      pp_pres,pp_var, pp_qc = p.read(var_fl  ,sourcedata='ppcon'  ) # force to read ppcon
                      if var_fl =='BBP700': pp_var= bellacicco_conversion(pp_var, zlevels_out) 
                      ppcon_varinterp = np.interp(zlevels_out, pp_pres, pp_var)
                      if var_fl in ['CHLA', 'BBP700', 'POC']: #ppcon plotted as 0-200m profile   
                         ax.plot(ppcon_varinterp[zlevels_out<=200] ,zlevels_out[zlevels_out<=200], COLOR_LIST[-1]  )
                      else:
                         ax.plot(ppcon_varinterp,zlevels_out, COLOR_LIST[-1]  )

                      ax.plot(float_var,zlevels_out, COLOR_LIST[2])

                   if p._my_float.status_profile(var_fl) =='I': 
                      ax.plot(float_var,zlevels_out, COLOR_LIST[2] )    # insitu only

                   ax.plot(  mod_f[var],zlevels_out, COLOR_LIST[0])
                   ax.plot(  mod_a[var],zlevels_out, COLOR_LIST[1])  
                
               else: #probabilm si puo togliere
                   print( LIST_AVA_PARA )
                   ax.plot(float_f[var],zlevels_out,COLOR_LIST[2])
                   ax.plot(  mod_f[var],zlevels_out,COLOR_LIST[0] )
                   ax.plot(  mod_a[var],zlevels_out,COLOR_LIST[1]) 

            else: # doxy temp sal
               ax.plot(float_f[var],zlevels_out,COLOR_LIST[2])
               ax.plot(  mod_f[var],zlevels_out,COLOR_LIST[0] )
               ax.plot(  mod_a[var],zlevels_out,COLOR_LIST[1]) 

            ax.set_title(plotvarname[i])
            ax.invert_yaxis()

        pngfile = OUTDIR + filename[:-3] + ".png"
        fig.savefig(pngfile)
        pl.close(fig)
        
        
    else:
        print (filename, " matches only analyis")
        #copy the previous *png
        pngfile = PREVIOUS_DIR + filename[:-3] +  ".png"
        command = "cp " + pngfile + " " + OUTDIR
        os.system(command)
    