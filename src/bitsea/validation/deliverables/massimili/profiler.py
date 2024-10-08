#!/usr/bin/env python
# Author: Giorgio Bolzon <gbolzon@ogs.trieste.it>
# Script to generate profiles of model files in
# the same time and locations where instruments
# such as bioFloats, mooring or vessels have been found.

# When imported, this scripts only defines settings for matchup generation.
from bitsea.instruments.lovbio_float import FloatSelector
from bitsea.static.Massimili_reader import MassimiliReader
from bitsea.instruments.matchup_manager import Matchup_Manager
from bitsea.commons.time_interval import TimeInterval
from bitsea.commons.Timelist import TimeList
from bitsea.basins.region import Rectangle
import os
# location of input big ave files, usually the TMP directory.
# ave files are supposed to have N3n, O2o and chl

OPA_HOME='/marconi_scratch/userexternal/ateruzzi/DA_FLOAT_SAT/RUN_FLOAT_2015_01/'
INPUTDIR    = OPA_HOME + 'wrkdir/MODEL/AVE_FREQ_1/'
aggregatedir= OPA_HOME + 'wrkdir/POSTPROC/output/AVE_FREQ_1/TMP/'
# output directory, where aveScan.py will be run.

BASEDIR    = OPA_HOME +   'wrkdir/POSTPROC/MASSIMILI_VALID/PROFILATORE/'



DATESTART = '20150101'
DATE__END = '20160101'

T_INT = TimeInterval(DATESTART,DATE__END, '%Y%m%d')
TL = TimeList.fromfilenames(T_INT, INPUTDIR,"ave*.nc",filtervar="N1p")
N = MassimiliReader()
ALL_PROFILES = N.Selector(None,T_INT, Rectangle(-6,36,30,46))


vardescriptorfile=os.getcwd() +  "/VarDescriptor.xml"

#This previous part will be imported in matchups setup.

# The following part, the profiler, is executed once and for all.
# It might take some time, depending on length of simulation or size of files.
if __name__ == '__main__':
    # Here instruments time and positions are read as well as model times
    M = Matchup_Manager(ALL_PROFILES,TL,BASEDIR)


    profilerscript = BASEDIR + 'jobProfiler.sh'
    M.writefiles_for_profiling(vardescriptorfile, profilerscript, aggregatedir=aggregatedir) # preparation of data for aveScan

    M.dumpModelProfiles(profilerscript) # sequential launch of aveScan
