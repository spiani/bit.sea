import numpy as np
from commons.Timelist import TimeList
from commons.time_interval import TimeInterval
from commons.timerequestors import Clim_month
import SatManager as Sat

def var_sat_CCI_10gg(limstd, dayF, MyMesh, INDIR, OUTDIR):
  """
  Computes the Monthly surface variance of the 10-days averages
  The inputs file are within INDIR directory and the outputs will be placed
  within OUTDIR

  The mesh must be consistent with the data contained in INDIR
  """

  Timestart="19500101"
  Time__end="20500101"

  TI = TimeInterval(Timestart,Time__end,"%Y%m%d")
  TLCheck = TimeList.fromfilenames(TI, INDIR,"*.nc",prefix='',dateformat='%Y%m%d')
  MONTHLY_reqs=[Clim_month(i) for i in range(1,13)]

  print "number of requests: ", len(MONTHLY_reqs), " inputFreq: ", TLCheck.inputFrequency

  jpi = MyMesh.jpi
  jpj = MyMesh.jpj

  Chl = np.zeros((12,jpj,jpi), dtype=float)
  ChlSquare = np.zeros((12,jpj,jpi), dtype=float)
  Var2D = np.zeros((12,jpj,jpi), dtype=float)

  for req in MONTHLY_reqs:
    ii, w = TLCheck.select(req)
    print ii, "\n"
  
    nFiles = len(ii)
    M  = np.zeros((nFiles,jpj,jpi),np.float32)
    M2 = np.zeros((nFiles,jpj,jpi),np.float32)
    
    for iFrame, j in enumerate(ii):
        inputfile = TLCheck.filelist[j]
        CHL = Sat.readfromfile(inputfile,'CHL')
        M[iFrame,:,:]  = CHL
        M2[iFrame,:,:] = CHL*CHL
    
    MonthIndex = req.month-1
    Chl[MonthIndex,:,:] = Sat.WeightedAverager(M,w)
    ChlSquare[MonthIndex,:,:] = Sat.WeightedAverager(M2,w)

  for ii in range(0,12):
    Var2D = ChlSquare(ii,0:,0:) - Chl(ii,0:,0:)

  print "\n\tDone :)\n"

if __name__ == "__main__":

    from postproc.masks import Mesh24

    INDIR  = "/pico/scratch/userexternal/pdicerbo/WorkDir/AveSat24/Checked_10Days_SatInterp24/"
    OUTDIR = "/pico/scratch/userexternal/pdicerbo/WorkDir/AveSat24/VarSat10Days/"
    limstd = 2
    dayF   = 10

    var_sat_CCI_10gg(limstd, dayF, Mesh24, INDIR, OUTDIR)