import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    Needs a profiler.py, already executed.
    Produces a file, containing timeseries for some statistics, for each wmo.
    In the outputdir, two new directories will be created, in order to store the output of check.
    - nitrate_check/
    - chla_check/
    ''', formatter_class=argparse.RawTextHelpFormatter)


    parser.add_argument(   '--maskfile', '-m',
                                type = str,
                                default = "/marconi_scratch/userexternal/lfeudale/Maskfiles/meshmask.nc",
                                required = False,
                                help = ''' Path of maskfile''')
    
    parser.add_argument(   '--basedir', '-b',
                                type = str,
                                default = "/marconi_scratch/userexternal/lfeudale/Maskfiles/meshmask.nc",
                                required = True,
                                help = ''' Path of maskfile''')    

    parser.add_argument(   '--outdir', '-o',
                                type = str,
                                default = None,
                                required = True,
                                help = "")

    return parser.parse_args()

args = argument()

from bitsea.commons.mesh import Mesh
from bitsea.commons.Timelist import TimeList
from bitsea.instruments.matchup_manager import Matchup_Manager
from bitsea.instruments.var_conversions import FLOATVARS
from bitsea.commons.utils import addsep
from bitsea.commons.layer import Layer
from bitsea.basins.region import Rectangle
# from bitsea.validation.online.metrics import *
from metrics2 import *
from bitsea.validation.online.SingleFloat_vs_Model_Stat_Timeseries_IOnc import dumpfile
from bitsea.Float.oxygen_saturation import *
import datetime
from bitsea.instruments import check




BASEDIR = addsep(args.basedir)
OUTDIR = addsep(args.outdir)
Check_obj_nitrate = check.check(OUTDIR + "nitrate_check/")
Check_obj_chl     = check.check(OUTDIR + "chla_check/")
Check_obj_phytoC = check.check(OUTDIR + "phytoC_check/")
Check_obj_oxygen = check.check(OUTDIR + "oxygen_check/")


TheMask = Mesh.from_file(args.maskfile, read_e3t=True)

TL = TimeList.fromfilenames(None, BASEDIR + "PROFILES/","ave*.nc")
deltaT= datetime.timedelta(hours=12)
TI = TimeInterval.fromdatetimes(TL.Timelist[0] - deltaT, TL.Timelist[-1] + deltaT)
ALL_PROFILES = bio_float.FloatSelector(None, TI, Rectangle(-6,36,30,46))


class variable:
    def __init__(self, name, extrap, check_obj):
        """ Arguments:
        * name *  string, like N3n
        * extrap * logical
        * check_obj * a check object defined in instruments.check
        """
        self.name = name
        self.extrap = extrap
        self.check_obj = check_obj

layer=Layer(0,200)
layer300=Layer(0,350)
layer1000=Layer(200,1000)

P_l = variable('P_l', True, Check_obj_chl)
N3n = variable('N3n', False, Check_obj_nitrate)
O2o = variable('O2o', False, Check_obj_oxygen)
P_c = variable('P_c', False, Check_obj_phytoC)
VARLIST = [P_l,N3n,O2o,P_c]


nVar = len(VARLIST)

METRICS = ['Int_0-200','Corr','DCM','z_01','Nit_1','SurfVal','dNit_dz','CM','O2o_sat','OMZ','max_O2']
nStat = len(METRICS)

M = Matchup_Manager(ALL_PROFILES,TL,BASEDIR)


iz200 = TheMask.getDepthIndex(200)+1 # Max Index for depth 200m
iz300 = TheMask.getDepthIndex(350)+1 # Max Index for depth 300m for Nitracl def
iz10 = TheMask.getDepthIndex(10.8)+1
iz1000 = TheMask.getDepthIndex(1000)+1 # Max Index for depth 1000

for V in VARLIST:
    var_mod=V.name
    var = FLOATVARS[var_mod]

    Profilelist = bio_float.FloatSelector(var, TI, Rectangle(-6,36,30,46))
    wmo_list=bio_float.get_wmo_list(Profilelist)
    for iwmo, wmo in enumerate(wmo_list):
        OUTFILE = "%s%s_%s.nc" %(OUTDIR, var_mod, wmo )
        print (OUTFILE, flush=True)
        list_float_track=bio_float.filter_by_wmo(Profilelist,wmo)
        nTime = len(list_float_track)
        A_float = np.zeros(( nTime, nStat), np.float32 ) * np.nan
        A_model = np.zeros(( nTime, nStat), np.float32 ) * np.nan

        for itime in range(nTime):
            if "gm200" in locals(): del gm200
            if "gm300" in locals(): del gm300
            p=list_float_track[itime]
            if p.available_params.find(var)<0 : continue

          # Pres,Profile,Qc=p.read(var,var_mod=var_model) # IT IS NOT USED; LEFT JUST FOR CHECK

            GM = M.getMatchups2([p], TheMask.zlevels, var_mod, interpolation_on_Float=False,checkobj=V.check_obj, extrapolation=V.extrap)


            if GM.number() == 0 :
                print (p.ID() + " excluded")
                continue
            gm200 = GM.subset(layer)
            gm300 = GM.subset(layer300)
            gm1000=GM.subset(layer1000)
 

            nLevels = gm200.number()
            izmax = min(nLevels,iz200)
  
            nLevels300 = gm300.number()
            izmax300 = min(nLevels300,iz300)

            nLevels1000 = gm1000.number()
            izmax1000 = min(nLevels1000,iz1000)

            # INTEGRAL 
            A_float[itime,0] =  np.nansum(gm200.Ref  *TheMask.dz[:izmax])/TheMask.dz[:izmax].sum() # Integral
            A_model[itime,0] =  np.nansum(gm200.Model*TheMask.dz[:izmax])/TheMask.dz[:izmax].sum() # Integral

            # SURF VALUE
            A_float[itime,5] = gm200.Ref[0] # Surf Value
            A_model[itime,5] = gm200.Model[0] # Surf Value

           # DCM/MWB
            if var_mod == "P_l":
                if 4. <= p.time.month <= 10:
                    A_float[itime,7], A_float[itime,2] = find_DCM(gm200.Ref  ,gm200.Depth) # CM, DCM
                    A_model[itime,7], A_model[itime,2] = find_DCM(gm200.Model,gm200.Depth) # CM, DCM
            
                if p.time.month in [1,2,3]:
                    A_float[itime,3] = find_WBL(gm200.Ref  ,gm200.Depth) # WBL
                    A_model[itime,3] = find_WBL(gm200.Model,gm200.Depth) # WBL

           # NITRACL1/NITRACL2 
            if var_mod == "N3n":
                # NOTA: level 350
                A_float[itime,4] = find_NITRICL(gm300.Ref  ,gm300.Depth) # Nitricline
                A_model[itime,4] = find_NITRICL(gm300.Model,gm300.Depth) # Nitricline

                A_float[itime,6],_ = find_NITRICL_dz_max(gm300.Ref  ,gm300.Depth) # dNit/dz
                A_model[itime,6],_ = find_NITRICL_dz_max(gm300.Model,gm300.Depth) # Nitricline

            if var_mod == "O2o":
                A_float[itime,8] = oxy_sat(p)

                if len(gm1000.Ref) > 1:
                    A_float[itime,9] = find_OMZ(gm1000.Ref, gm1000.Depth) # Oxygen Minimum Zone
                    A_model[itime,9] = find_OMZ(gm1000.Model, gm1000.Depth) # Oxygen Minimum Zone 

                    A_float[itime,10] = find_maxO2(gm300.Ref, gm300.Depth) # Oxygen Max depth
                    A_model[itime,10] = find_maxO2(gm300.Model, gm300.Depth) # Oxygen Max depth


            A_float[itime,1] = gm200.correlation() # Correlation
            A_model[itime,1] = gm200.correlation() # Correlation

        dumpfile(OUTFILE,A_float,A_model,METRICS)
