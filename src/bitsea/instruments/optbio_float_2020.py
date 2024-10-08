import scipy.io.netcdf as NC
import numpy as np
import datetime
import os
import matplotlib.pyplot as pl
from bitsea.commons.utils import addsep

from instrument import Instrument, Profile
from bitsea.mhelpers.pgmean import PLGaussianMean
meanObj = PLGaussianMean(5,1.0)

mydtype= np.dtype([
          ('file_name','S200'),
          ('lat',np.float32),
          ('lon',np.float32),
          ('time','S17'),
          ('parameters','S200')] )
GSS_DEFAULT_LOC = "/gss/gss_work/DRES_OGS_BiGe/Observations/TIME_RAW_DATA/STATIC/"
STATIC_REPO = addsep(os.getenv("STATIC_REPO",GSS_DEFAULT_LOC))
FloatIndexer=addsep(STATIC_REPO) + "Float_OPT_2020/Float_Index.txt"
INDEX_FILE=np.loadtxt(FloatIndexer,dtype=mydtype, delimiter=",",ndmin=1)

class BioFloatProfile(Profile):
    def __init__(self, time, lon, lat, my_float, available_params,mean=None):
        self.time = time
        self.lon = lon
        self.lat = lat
        self._my_float = my_float
        self.available_params = available_params
        self.mean = mean

    def __eq__(self, other):
        if isinstance(other, BioFloatProfile):
            if (self.lon == other.lon) & (self.lat == other.lat) & (self.time == other.time):
                return self._my_float == other._my_float
            else:
                return False
        else:
            return False

    def read(self,var):
        '''
        Reads profile data from file. Wrapper for BioFloat.read()

        Takes var as string
              read_adjusted as logical
        Returns 3 numpy arrays: Pres, Profile, Qc '''

        return self._my_float.read(var, mean=self.mean)

    def name(self):
        '''returns a string, the wmo of the associated BioFloat.
        '''
        return self._my_float.wmo

    def ID(self):
        return  self.name() + "_" + self.time.strftime("%Y%m%d-%H:%M:%S_") + str(self.lon) + "_"+ str(self.lat)


class BioFloat(Instrument):

    default_mean = None

    def __init__(self,lon,lat,time,filename,available_params):
        self.lon = lon
        self.lat = lat
        self.time = time
        self.filename = filename
        self.available_params = available_params
        #istart=filename.index("/",filename.index('Float_OPT_2019'))
        #iend  =filename.index("/",istart+1)
        wmo, cycle = os.path.basename(filename).rsplit("_")
        self.wmo = wmo[2:]
        self.cycle = int(cycle[:3])
        #self.wmo = filename[istart+1:iend]
        #cycle = os.path.basename(filename).rsplit("_")[2]
        #self.cycle = int(cycle)


    def __eq__(self,other):
        if isinstance(other, BioFloat):
            if (self.filename  == other.filename):
                return (self.lon == other.lon ) & (self.lat == other.lat) & (self.time == other.time)
            else:
                return False
        else:
            return False



    def read_raw(self,var):
        '''
        Reads data from file
        Returns 2 numpy arrays: Pres, Profile
        '''
        ncIN=NC.netcdf_file(self.filename,'r')
        Pres    = ncIN.variables['PRES_'+var].data.copy()
        Profile = ncIN.variables[        var].data.copy()
        ncIN.close()

        return Pres, Profile

    def read(self, var, mean=None):
        '''

        Reads profile data from file, applies a rarefaction and optionally a filter to the data

        Takes var as string
              read_adjusted as logical
        Returns 3 numpy arrays: Pres, Profile, Qc
        '''


        raw_pres, raw_prof   = self.read_raw(var)
        pres,index=np.unique(raw_pres,return_index=True)
        prof =  raw_prof[index]
        qc = np.ones_like(pres)*2
        #if var=='CHLA': prof = prof*0.5


        if pres.size ==0:
            return pres, prof, qc

        if mean == None:
            if BioFloat.default_mean != None:
                return pres, BioFloat.default_mean.compute(prof, pres), qc
            else:
                return pres, prof, qc
        else:
            return pres, mean.compute(prof, pres), mean.compute(qc,pres)


    def basicplot(self,Pres,profile):
        pl.figure()
        pl.plot(profile,Pres)
        pl.gca().invert_yaxis()
        pl.show(block=False)

    def plot(self,Pres,profile,fig=None,ax=None,**kwargs):
        '''
    Args:
        - * Pres    * : array of pressure
        - * profile * : array of profile values
        - * fig     * : a reference to a Figure object, if None a new Figure will be created.
        - * ax      * : a reference to an Axes object, if None a new axis will be created.

    Returns :
        A figure and an axis object

    Examples:
        fig, ax = f.plot(pres,profile)
        fig, ax = f.plot(pres,profile,fig,ax)
        fig, ax = f.plot(pres,profile,fig,ax, linestyle = 'dashed', linewidth = 2, color='green')

        '''
        if (fig is None) or (ax is None):
            fig , ax = pl.subplots()
        ax.plot(profile,Pres, **kwargs)
        if not ax.yaxis_inverted(): ax.invert_yaxis()
        return fig,ax

    def profiles(self, var, mean=None):
        return [BioFloatProfile(var, self.time, self.lon, self.lat, self, mean)]

    @staticmethod
    def from_file(filename):
        '''
        Returns the single Bio_Float instance corresponding to filename
        '''
        nFiles=INDEX_FILE.size
        for iFile in range(nFiles):
            timestr          = INDEX_FILE['time'][iFile]
            lon              = INDEX_FILE['lon' ][iFile]
            lat              = INDEX_FILE['lat' ][iFile]
            thefilename      = INDEX_FILE['file_name'][iFile]
            available_params = INDEX_FILE['parameters'][iFile]
            float_time = datetime.datetime.strptime(timestr,'%Y%m%d-%H:%M:%S')
            if filename.endswith(thefilename):
                return BioFloat(lon,lat,float_time,filename,available_params)
        return None

def profile_gen(lon,lat,float_time,filename,available_params):
    thefloat = BioFloat(lon,lat,float_time,filename,available_params)
    return BioFloatProfile(float_time,lon,lat, thefloat,available_params,meanObj)

def FloatSelector(var, T, region):
    '''
    Arguments:
       * var *    is a string indicating variable, 
                  if var is None, no selection is done about variable
       * T   *    is a TimeInterval instance or a timerequestors.Clim_season instance
                  or whatever object having a contains() method working as the TimeInteval one does.
       * region * is an instance of Region or its derived (Polygon, Basin, ...)

    Returns:
        a list of BioFloatProfile objects.
    Caveats:
       In order to work on dataset different from the cineca DRES archive
       /gss/gss_work/DRES_OGS_BiGe/Observations/TIME_RAW_DATA/STATIC/
       remember to define the environment variable STATIC_REPO
       export STATIC_REPO=/some/path/with/ Float_opt_2019/ Float_opt_2020/
    '''

    nFiles=INDEX_FILE.size
    selected = []
    for iFile in range(nFiles):
        timestr          = INDEX_FILE['time'][iFile]
        lon              = INDEX_FILE['lon' ][iFile]
        lat              = INDEX_FILE['lat' ][iFile]
        filename         = INDEX_FILE['file_name'][iFile]
        available_params = INDEX_FILE['parameters'][iFile]
        float_time = datetime.datetime.strptime(timestr,'%Y%m%d-%H:%M:%S')
        filename = STATIC_REPO + "Float_OPT_2020/" + filename

        if var is None :
            VarCondition = True
        else:
            VarCondition = var in available_params

        if VarCondition:
            if T.contains(float_time) and region.is_inside(lon, lat):
                thefloat = BioFloat(lon,lat,float_time,filename,available_params)
                selected.append(BioFloatProfile(float_time,lon,lat, thefloat,available_params,None))

    return selected

def get_wmo_list(Profilelist):
    '''
     Argument:
      * Profilelist * list of Profile objects

      Returns:
         a list of wmo strings
    '''
    wmo_set=set()
    for p in Profilelist:
        wmo_set.add(p._my_float.wmo)
    return list(wmo_set)

def filter_by_wmo(Profilelist,wmo):
    '''

    Subsetter, filtering by wmo

     Arguments:
      * Profilelist * list of Profile objects
      * wmo         * string

      Returns:
        a list of Profile Objects
    '''

    return [p for p in Profilelist if p._my_float.wmo == wmo]


def from_profile(profile, verbose=True):
    '''
    Arguments:
    * profile * a profile object (float_opt_2019, 
    * verbose     * logical, used to print lov files that don't have a corresponding in coriolis

    Returns:
    *  p * a LOV BioFloatProfile object
    '''
    wmo = profile._my_float.wmo
    INDEXES=[]
    for iFile, filename in enumerate(INDEX_FILE['file_name']):
        if filename.startswith(wmo):
            INDEXES.append(iFile)
    A = INDEX_FILE[INDEXES]
    nFiles = len(A)
    if nFiles==0: return None
    DELTA_TIMES = np.zeros((nFiles,), np.float32)
    for k in range(nFiles):
        float_time =datetime.datetime.strptime(A['time'][k],'%Y%m%d-%H:%M:%S')
        deltat = profile.time - float_time
        DELTA_TIMES[k] = deltat.total_seconds()
    min_DeltaT = np.abs(DELTA_TIMES).min()
    if min_DeltaT > 3600*3 :
        if verbose: print "no FLOAT_OPT_2020 file corresponding to "  + profile._my_float.filename
        return None
    F = (A['lon'] - profile.lon)**2 + (A['lat'] - profile.lat)**2 +  DELTA_TIMES**2
    iFile = F.argmin()
    timestr          = A['time'][iFile]
    lon              = A['lon' ][iFile]
    lat              = A['lat' ][iFile]
    filename         = A['file_name'][iFile]
    available_params = A['parameters'][iFile]
    float_time = datetime.datetime.strptime(timestr,'%Y%m%d-%H:%M:%S')
    return profile_gen(lon, lat, float_time, filename, available_params)


if __name__ == '__main__':
    from bitsea.basins.region import Rectangle
    from bitsea.commons.time_interval import TimeInterval

    var = 'BBP700'
    TI = TimeInterval('20120101','20170130','%Y%m%d')
    R = Rectangle(-6,36,30,46)

    PROFILE_LIST=FloatSelector(var, TI, R)
    filename="/gss/gss_work/DRES_OGS_BiGe/Observations/TIME_RAW_DATA/STATIC/Float_OPT_2020/6903197/SD6903197_079.nc"
    F=BioFloat.from_file(filename)


    for ip, p in enumerate(PROFILE_LIST):
        Pres,V, Qc = p.read(var)
        ii=Pres>100
        deriv_1 = np.diff(V[ii])
        if (deriv_1>0).any():
            print "First derivative > 0 at profile ", ip
            import sys
            sys.exit()


        if Pres.min()>0:
            print Pres.min()

    wmo_list= get_wmo_list(PROFILE_LIST)
    for wmo in wmo_list:
        sublist = filter_by_wmo(PROFILE_LIST, wmo)
