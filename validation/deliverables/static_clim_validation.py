import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    Generates in output directory two files ( model and ref) 
    containing [nSub, nLayers] arrays of climatologies.
    These arrays will be used in the next step to generate the following metrics:

    PHO-LAYER-Y-CLASS4-CLIM-BIAS/RMSD
    NIT-LAYER-Y-CLASS4-CLIM-BIAS/RMSD
     DO-LAYER-Y-CLASS4-CLIM-BIAS/RMSD
    ALK-LAYER-Y-CLASS4-CLIM-BIAS/RMSD
    DIC-LAYER-Y-CLASS4-CLIM-BIAS/RMSD

    ALK-PROF-Y-CLASS4-CLIM-CORR-BASIN
    DIC-PROF-Y-CLASS4-CLIM-CORR-BASIN
    ''', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(   '--inputdir','-i',
                                type = str,
                                required = True,
                                help = '')

    parser.add_argument(   '--outdir', '-o',
                                type = str,
                                default = None,
                                required = True,
                                help = "")
    parser.add_argument(   '--maskfile', '-m',
                                type = str,
                                default = None,
                                required = True,
                                help = "")
    parser.add_argument(   '--starttime','-s',
                                type = str,
                                required = True,
                                help = 'start date in yyyymmdd format')
    parser.add_argument(   '--endtime','-e',
                                type = str,
                                required = True,
                                help = 'start date in yyyymmdd format')   
    return parser.parse_args()

args = argument()

import numpy as np
from commons.time_interval import TimeInterval
from commons.Timelist import TimeList
from timeseries.plot import Hovmoeller_matrix
from commons.mask import Mask
from commons.layer import Layer
from basins import V2 as basV2
from static import climatology
from commons.utils import addsep
from matchup.statistics import matchup

LayerList = [Layer(0,10), Layer(10,30), Layer(30,60), Layer(60,100), Layer(100,150), Layer(150,300), Layer(300,600), Layer(600,1000)]

INPUTDIR=addsep(args.inputdir)
OUTDIR = addsep(args.outdir)
TI = TimeInterval(args.starttime,args.endtime,"%Y%m%d")

TheMask= Mask(args.maskfile, loadtmask=False)
jpk,jpj,jpi = TheMask.shape
z = -TheMask.zlevels

z_clim = np.array([-(l.bottom+l.top)/2  for l in LayerList])

TL = TimeList.fromfilenames(TI, INPUTDIR, "ave*nc")

def Layers_Mean(Pres,Values,LayerList):
    '''
    Performs mean of profile along layers.

    Arguments:
    * Pres      * numpy array of pressures
    * Values    * numpy array of concetrations
    * LayerList * list of layer objects
    Returns :
    * MEAN_LAY * [nLayers] numpy array, mean of each layer
    '''
    MEAN_LAY = np.zeros(len(LayerList), np.float32)

    for ilayer, layer in enumerate(LayerList):
        ii = (Pres>=layer.top) & (Pres<=layer.bottom)
        if (ii.sum()> 1 ) :
            local_profile = Values[ii]
            MEAN_LAY[ilayer] = np.mean(local_profile)
    return MEAN_LAY

VARLIST=['N1p','N3n','O2o','Ac','DIC']
SUBlist = basV2.Pred.basin_list
nSub = len(SUBlist)
nLayers = len(LayerList)
METRICvar = {'N1p':'PHO',
             'N3n':'NIT',
             'O2o':'DO',
             'Ac':'ALK',
             'DIC':'DIC'}



for ivar, var in enumerate(VARLIST):
    print "" 
    print var
    metric = METRICvar[var] + "-LAYER-Y-CLASS4-CLIM-"
    print metric + "BIAS", metric + "RMSD"
    CLIM_REF_static = climatology.get_climatology(var,SUBlist, LayerList)
    
    CLIM_MODEL = np.zeros((nSub, nLayers))
    for iSub, sub in enumerate(SUBlist):
        Mean_profiles,_,_ = Hovmoeller_matrix(TL.Timelist,TL.filelist, var, iSub, coast=1, stat=0, depths=np.arange(jpk)) #72 nFiles
        mean_profile = Mean_profiles.mean(axis=1)
        mean_profile[mean_profile==0]=np.nan
        CLIM_MODEL[iSub,:] = Layers_Mean(TheMask.zlevels, mean_profile,LayerList)
    np.save(OUTDIR + var + "ref_clim", CLIM_REF_static)
    np.save(OUTDIR + var + "mod_clim", CLIM_MODEL)
    for ilayer, layer in enumerate(LayerList):
        refsubs = CLIM_REF_static[:,ilayer]
        modsubs =      CLIM_MODEL[:,ilayer]
        bad = np.isnan(refsubs) | np.isnan(modsubs)
        good = ~bad
        m = matchup(modsubs[good], refsubs[good])
        print  m.bias(), m.RMSE()





PresDOWN=np.array([25,50,75,100,125,150,200,400,600,800,1000,1500,2000,2500])
LayerList_2=[]
top = 0
for bottom in PresDOWN:
    LayerList_2.append(Layer(top, bottom))
    top = bottom
nLayers = len(LayerList_2)

for var in ['Ac','DIC']:
    metric = METRICvar[var] + "-PROF-Y-CLASS4-CLIM-CORR-BASIN"
    print ""
    print metric
    CLIM_REF_static = climatology.get_climatology(var,SUBlist, LayerList_2)
    CLIM_MODEL = np.zeros((nSub, nLayers))
    for iSub, sub in enumerate(SUBlist):
        Mean_profiles,_,_ = Hovmoeller_matrix(TL.Timelist,TL.filelist, var, iSub, coast=1, stat=0, depths=np.arange(jpk)) #72 nFiles
        mean_profile = Mean_profiles.mean(axis=1)
        mean_profile[mean_profile==0]=np.nan
        CLIM_MODEL[iSub,:] = Layers_Mean(TheMask.zlevels, mean_profile,LayerList_2)
    np.save(OUTDIR + var + "ref_clim14", CLIM_REF_static)
    np.save(OUTDIR + var + "mod_clim14", CLIM_MODEL)
    for isub, sub in enumerate(SUBlist):
        refsubs = CLIM_REF_static[isub,:]
        modsubs =      CLIM_MODEL[isub,:]
        bad = np.isnan(refsubs) | np.isnan(modsubs)
        good = ~bad
        ngoodlayers=good.sum()
        if ngoodlayers>0:
            m = matchup(modsubs[good], refsubs[good])
            print sub.name, ngoodlayers, m.correlation()
        else:
            print sub.name, ngoodlayers, np.nan