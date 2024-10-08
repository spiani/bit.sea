import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    Weighted averager for sat files for weekly average only.
    It works with one mesh, without performing interpolations.
    Files with dates used for the average provided (dirdates).
    ''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(   '--checkdir', '-i',
                                type = str,
                                required = True,
                                help = ''' CHECKED sat directory, e.g. /gss/gss_work/DRES_OGS_BiGe/Observations/TIME_RAW_DATA/ONLINE/SAT/MODIS/DAILY/CHECKED/'''

                                )
    parser.add_argument(   '--outdir', '-o',
                                type = str,
                                required = True,
                                help = ''' OUT average dates sat directory'''

                                )

    parser.add_argument(   '--dirdates', '-d',
                                type = str,
                                required = True,
                                help = ''' OUT dates sat directory'''

                                )

    parser.add_argument(   '--dirpmap', '-p',
                                type = str,
                                required = True,
                                help = ''' OUT dates sat directory'''

                                )

    parser.add_argument(   '--mesh', '-m',
                                type = str,
                                required = True,
                                choices = ['SatOrigMesh','V4mesh','V1mesh','KD490mesh','SAT1km_mesh', 'Mesh24', 'Mesh4'],
                                help = ''' Name of the mesh of sat ORIG and used to dump checked data.'''
                                )

    parser.add_argument(   '--timeaverage', '-t',
                                type = str,
                                required = True,
                                choices = ['weekly_tuesday','weekly_friday','weekly_monday','weekly_thursday'],
                                help = ''' Name of the mesh of sat ORIG and used to dump checked data.'''
                                )

    parser.add_argument(   '--stdweight', '-s',
                                type = str,
                                required = True,
                                help = ''' Std for Gaussian weight (n. days of time correlation'''
                                )

    return parser.parse_args()

args = argument()


from bitsea.commons.Timelist import TimeList
from bitsea.commons.time_interval import TimeInterval
from bitsea.postproc import masks
import numpy as np
import os
import bitsea.Sat.SatManager as Sat
from bitsea.commons.utils import addsep

try:
    from mpi4py import MPI
    comm  = MPI.COMM_WORLD
    rank  = comm.Get_rank()
    nranks =comm.size
    isParallel = True
except:
    rank   = 0
    nranks = 1
    isParallel = False

CHECKDIR = addsep(args.checkdir)
OUTDIR   = addsep(args.outdir)
DIRDATES = addsep(args.dirdates)
DIRPMAP  = addsep(args.dirpmap)
std = float(args.stdweight)
maskSat = getattr(masks,args.mesh)

reset = False

Timestart="19500101"
Time__end="20500101"
TI = TimeInterval(Timestart,Time__end,"%Y%m%d")
TLCheck = TimeList.fromfilenames(TI, CHECKDIR,"*.nc",prefix='',dateformat='%Y%m%d')
suffix = os.path.basename(TLCheck.filelist[0])[8:]


if args.timeaverage == 'weekly_tuesday' : TIME_reqs=TLCheck.getWeeklyList(2)
if args.timeaverage == 'weekly_friday'  : TIME_reqs=TLCheck.getWeeklyList(5)
if args.timeaverage == 'weekly_monday'  : TIME_reqs=TLCheck.getWeeklyList(1)
if args.timeaverage == 'weekly_thursday': TIME_reqs=TLCheck.getWeeklyList(4)

jpi = maskSat.jpi
jpj = maskSat.jpj

counter = 0
MySize = len(TIME_reqs[rank::nranks])

for req in TIME_reqs[rank::nranks]:
    counter = counter + 1

    outfile = req.string + suffix
    outpathfile = OUTDIR + outfile

    ii,ww = TLCheck.selectWeeklyGaussWeights(req,std)
    nFiles = len(ii)

    if os.path.exists(outpathfile):
        outdates = DIRDATES + req.string + 'weekdates.txt'
        weekdates = np.loadtxt(outdates,dtype=str)
        nDates = len(weekdates)
    
        if nFiles>nDates:
            print 'Not skipping ' + req.string
        else:
            conditionToSkip = (os.path.exists(outpathfile)) and (not reset)
            if conditionToSkip: continue

    print outfile
    dateweek = []
    if nFiles < 3 : 
        print req
        print "less than 3 files"
        filedates = DIRDATES + req.string + 'weekdates.txt'
        print(filedates)
        np.savetxt(filedates,dateweek,fmt='%s')
        continue
    M = np.zeros((nFiles,jpj,jpi),np.float32)
    for iFrame, j in enumerate(ii):
        inputfile = TLCheck.filelist[j]
        CHL = Sat.readfromfile(inputfile)
        M[iFrame,:,:] = CHL
        idate = TLCheck.Timelist[j]
        date8 = idate.strftime('%Y%m%d')
        dateweek.append(date8)
    CHL_OUT = Sat.WeightedLogAverager(M,ww)
    Sat.dumpGenericNativefile(outpathfile, CHL_OUT, varname='CHL', mesh=maskSat)

    filepmap = DIRPMAP + req.string + 'npmap.nc'
    maskM = M>0.
    npM = np.sum(maskM,0)
    Sat.dumpGenericNativefile(filepmap, npM, varname='npWeek',mesh=maskSat)
    print(filepmap)

    filedates = DIRDATES + req.string + 'weekdates.txt'
    print(filedates)
    np.savetxt(filedates,dateweek,fmt='%s')

    print "\trequest ", counter, " of ", MySize, " done by rank ", rank

