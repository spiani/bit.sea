import postproc.Timelist as Timelist
import postproc.IOnames as IOnames
import numpy as np
import SatManager as Sat
import matchup.matchup as matchup
#from postproc.maskload import *
import scipy.io.netcdf as NC


MODEL_DIR="/gpfs/work/OGS_prod/CalVal/Q_REP_MODEL_FORECAST/"
REF_DIR  = "/gss/gss_work/DRES_OGS_BiGe/Observations/TIME_RAW_DATA/ONLINE/SAT/MODIS/WEEKLY/"

Timestart="20150701"
Time__end="20151001"
IonamesFile = '../postproc/IOnames_sat.xml'
IOname = IOnames.IOnames(IonamesFile)
model_TL = Timelist.TimeList(Timestart,Time__end, MODEL_DIR,"*.nc",IonamesFile)
ngib=52

for itime, time in enumerate(model_TL.Timelist[:1]):
    satfile = REF_DIR + time.strftime(IOname.Input.dateformat) + IOname.Output.suffix + ".nc"
    modfile = model_TL.filelist[itime]
     
    ncIN = NC.netcdf_file(modfile,'r')
    For = ncIN.variables['chl'].data[0,0,:,:].copy().astype(np.float64)
    ncIN.close()
    
    Sat16 = Sat.convertinV4format(Sat.readfromfile(satfile)).astype(np.float64)
    Sat16 = Sat16[:,ngib:]
    
    cloudsLand = np.isnan(Sat16)
    modelLand  = For > 1.0e+19
    nodata     = cloudsLand | modelLand
    M = matchup.matchup(For[~nodata], Sat16[~nodata])
    print M.bias()
    
    