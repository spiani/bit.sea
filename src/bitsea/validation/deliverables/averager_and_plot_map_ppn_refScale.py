import argparse
from bitsea.utilities.argparse_types import date_from_str
from bitsea.utilities.argparse_types import existing_dir_path, existing_file_path
def argument():
    parser = argparse.ArgumentParser(description = '''
    Generates png maps, based on matplotlib.imshow(), of time averaged fields
    
    Brief description of the algorithm:
    INPUTS                                               OPERATOR              OUTPUT
    (InputDir, varname, StartTime, EndTime)  ---->     time average       ---> 3D field
    (3d_field, Layer list )                  ----> vertical mean/integral ---> 2d map
    
    
    Example of output file: 
    ppn_2021_Int0000-0200m-0000m_refScale.png
    ppn_2021_mean_basin.txt
    
    Caveats:
    A unit conversion is performed, about ppn.
    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(   '--outdir', '-o',
                            type = existing_dir_path,
                            required =True,
                            help = ''' Output dir'''
                            )

    parser.add_argument(   '--inputdir', '-i',
                            type = existing_dir_path,
                            required = True,
                            help = 'Input dir')

    parser.add_argument(   '--varname', '-v',
                                type = str,
                                required = True,
                                default = '',
                                choices = ['P_l','P_i','N1p', 'N3n', 'O2o', 'pCO2','PH','pH','ppn','P_c','Ac','DIC'] )
    parser.add_argument(   '--plotlistfile', '-l',
                                type = str,
                                required = True,
                                help = '''Plotlist_bio.xml"
                                ''')
    parser.add_argument(   '--maskfile', '-m',
                                type = existing_file_path,
                                required = True,
                                help = 'Path of the mask file')
    parser.add_argument(   '--optype', '-t',
                                type = str,
                                required = True,
                                default = '',
                                choices = ['integral','mean'],
                                help ="  INTEGRALE:  * heigth of the layer, MEDIA    :  average of layer")
    parser.add_argument(   '--starttime','-s',
                                type = date_from_str,
                                required = True,
                                help = 'start date in yyyymmdd format')
    parser.add_argument(   '--endtime','-e',
                                type = date_from_str,
                                required = True,
                                help = 'start date in yyyymmdd format')      

    return parser.parse_args()
args = argument()

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl

from bitsea.commons.time_interval import TimeInterval
from bitsea.commons.Timelist import TimeList
from bitsea.commons.mask import Mask
from bitsea.commons.layer import Layer
from bitsea.layer_integral.mapbuilder import MapBuilder, Plot
from bitsea.commons.dataextractor import DataExtractor
from bitsea.commons.time_averagers import TimeAverager3D
from bitsea.layer_integral import coastline
import bitsea.commons.timerequestors as requestors
from bitsea.commons.xml_module import get_node_attr, get_subelements
from xml.dom import minidom
from bitsea.commons import netcdf3

xmldoc = minidom.parse(args.plotlistfile)


INPUTDIR  = args.inputdir
OUTPUTDIR = args.outdir
var       = args.varname

if  args.optype=='integral':
    maptype="Int"
else:
    maptype="Ave"

for lm in xmldoc.getElementsByTagName("LayersMaps"):
    for pdef in get_subelements(lm, "plots"):
        filevar = get_node_attr(pdef, "var")        
        if not filevar == var : continue
        PLOT = Plot(get_node_attr(pdef, "var"), get_node_attr(pdef, "longname"), get_node_attr(pdef, "plotunits"), [], [0,1] )
        for d in get_subelements(pdef, "depth"):
            levplot  = float(get_node_attr(d, "levplot")) 
            clim     = eval(get_node_attr(d, "clim"))
            L = Layer(get_node_attr(d,"top"), get_node_attr(d, "bottom"))
            PLOT.append_layer(L,clim=clim, mapdepthfilter=levplot)
            




clon,clat = coastline.get()
TheMask = Mask.from_file(args.maskfile)

CONVERSION_DICT={
         'ppn' : 365./1000,
         'O2o' : 1,
         'N1p' : 1,
         'N3n' : 1,
         'PH'  : 1,
         'pH'  : 1, 
         'pCO2': 1,
         'P_l' : 1,
         'P_c' : 1,
         'P_i' : 1,
	     'Ac'  : 1,
         'DIC' : 1
         }

MONTH_STRING = ["January","February","March","April","May","June","July","August","September","October","November","December"]
TI = TimeInterval.fromdatetimes(args.starttime,args.endtime)
if args.endtime.year > args.starttime.year:
    req_label=f"{args.starttime.year}_{args.endtime.year}"
else:
    req_label=f"{args.starttime.year}"


TL = TimeList.fromfilenames(TI, INPUTDIR,"ave*.nc",filtervar=var)
if TL.inputFrequency is None:
    TL.inputFrequency='monthly'
    print ("inputFrequency forced to monthly because of selection of single time")

req = requestors.Generic_req(TI)
indexes,weights = TL.select(req)


VARCONV=CONVERSION_DICT[var]
# setting up filelist for requested period -----------------
filelist=[]
for k in indexes:
    t = TL.Timelist[k]
    filename = INPUTDIR / ("ave." + t.strftime("%Y%m%d-%H:%M:%S") + "." + var + ".nc")
    filelist.append(filename)
# ----------------------------------------------------------
print ("time averaging ...")
M3d     = TimeAverager3D(filelist, weights, var, TheMask)
print ("... done.")
for il, layer in enumerate(PLOT.layerlist):
    z_mask = PLOT.depthfilters[il]
    z_mask_str = "-%04gm" %z_mask
    Lstr=layer.longname()

    filename = f"{var}_{req_label}_{maptype}{Lstr}{z_mask_str}_refScale"
    outfile=OUTPUTDIR / f"{filename}.png"
    print(outfile)

    De      = DataExtractor(TheMask,rawdata=M3d)

    if args.optype=='integral':
        integrated = MapBuilder.get_layer_integral(De, layer)
    else:
        integrated = MapBuilder.get_layer_average(De, layer)
    integrated=integrated * VARCONV


    mask=TheMask.mask_at_level(z_mask)
    clim=PLOT.climlist[il]
    integrated_masked=integrated*mask # taglio il costiero
    integrated_masked[integrated_masked==0]=np.nan # sostituisco gli 0 con i NAN

# X ppn:
    fig,ax = pl.subplots()
    fig.set_size_inches(10.0, 10.0*16/42)
    ax.set_position([0.08, 0.13, 0.78, 0.78])
    levels = [0, 25, 50, 75, 100, 125, 150, 175, 200, 300, 400, 500]
    # colors = ['navy','blue','royalblue','deepskyblue','aqua','lawngreen','greenyellow','gold','orange','red','maroon']
    colors = ['midnightblue','indigo','blue','royalblue','deepskyblue','aqua','greenyellow','gold','orange','red','maroon']
    # New corlors more similar to Lazzari et al. (2012)

    CS=ax.contourf(TheMask.xlevels, TheMask.ylevels,integrated_masked,levels,colors=colors)
    cbar=fig.colorbar(CS,ticks=levels)
    ax.set_xlim([-5,36])

    ax.set_ylim([30,46])
    ax.set_xlabel('Lon').set_fontsize(11)
    ax.set_ylabel('Lat').set_fontsize(12)
    ax.tick_params(axis='x', labelsize=10)
# CHANGE ACRONYM for NET PRIMARY PRODUCTION from "ppn" to "npp":
    if (var=="ppn"):
        ax.text(-4,44.5,'npp [' + PLOT.units() + ']',horizontalalignment='left',verticalalignment='center',fontsize=14, color='black')
        title = "%s %s %s" % (req_label, 'npp', layer.__repr__())
    else:
        ax.text(-4,44.5,var + ' [' + PLOT.units() + ']',horizontalalignment='left',verticalalignment='center',fontsize=14, color='black')
        title = "%s %s %s" % (req_label, var, layer.__repr__())

    ax.xaxis.set_ticks(np.arange(-2,36,6))
    ax.yaxis.set_ticks(np.arange(30,46,4))
##########
    #Draw coastline
    ax.plot(clon,clat, color='#000000',linewidth=0.5)
    ax.set_xlim([-6, 36])
    ax.set_ylim([30, 46])
#########
    ax.grid()
    if (var == "pH"): title = "%s %s %s" % (MONTH_STRING[TI.start_time.month - 1], "pH$\mathrm{_T}$", layer.__repr__())
    if (var == "pCO2"): title = "%s %s %s" % (MONTH_STRING[TI.start_time.month - 1], "pCO2", layer.__repr__())
    pl.suptitle(title)
    pl.savefig(outfile)
    pl.close(fig)
    if (var == "ppn"): 
        ncfile=OUTPUTDIR / f"{filename}.nc"
        netcdf3.write_2d_file(integrated_masked,"ppn",ncfile,TheMask)

        from bitsea.basins import V2 as OGS
        from bitsea.commons.submask import SubMask
        from bitsea.basins.basin import ComposedBasin
        from bitsea.commons.utils import writetable
        tablefile = OUTPUTDIR / f"{var}_{req_label}_mean_basin.txt"
        print(tablefile)
        OGSred = ComposedBasin('OGSred',[OGS.alb, \
                    OGS.swm1, OGS.swm2, OGS.nwm, OGS.tyr, \
                    OGS.adr, OGS.ion, OGS.lev , OGS.med], \
                    'Gruped Subbasin for ppn analysis')
        SUBlist = OGSred.basin_list
        nSub   = len(OGSred.basin_list)
        rows_names=[sub.name for sub in SUBlist]
        ppn_submean = np.zeros((nSub,1),np.float32)*np.nan
        for isub, sub in enumerate(OGSred):
            S = SubMask(sub, TheMask)
            mask2d=S.mask[0,:,:]
            ppn_submean[isub,0] = integrated_masked[mask2d].mean()
        
        writetable(tablefile,ppn_submean,rows_names,['mean'])
