import numpy as np
import os, sys
from commons.mask import Mask
from commons.submask import SubMask


annaCoast = False

maskfile    = os.getenv("MASKFILE"); 
if maskfile is None : 
    print "Error: Environment variable MASKFILE must be defined "
    sys.exit(1)

if annaCoast:
    kcoastfile  = os.getenv( "KCOASTFILE");
    if kcoastfile is None:
        print "Error: Environment variable KCOASTFILE must be defined "
        sys.exit(1)

TheMask=Mask(maskfile,ylevelsmatvar="gphit", xlevelsmatvar="glamt")
jpk,jpj,jpi = TheMask.shape


tmask   =  TheMask.mask
nav_lev =  TheMask.zlevels
Lon     =  TheMask.xlevels
Lat     =  TheMask.ylevels
area    =  TheMask.area
e3t     =  TheMask.dz


MEDmask      = tmask.copy()
MEDmask[:, Lon < -5.3] = False# Atlantic buffer 

mask200_2D   = TheMask.mask_at_level(200.0)
#mask200_2D[Lon < -5.3] = False # Atlantic buffer
mask200_3D = np.zeros((jpk,jpj,jpi),dtype=np.bool)
for i in range(jpk):
    mask200_3D[i,:,:]=mask200_2D

if annaCoast:
    # Read k means class for coastal areas
    kcoastmask = np.load(kcoastfile)
    kmask1_2D =  np.zeros((jpj,jpi),dtype=np.bool)
    kmask1_2D[kcoastmask==1] = True
    kmask2_2D =  np.zeros((jpj,jpi),dtype=np.bool)
    kmask2_2D[kcoastmask==2] = True
    kmask1 =  np.zeros((jpk,jpj,jpi),dtype=np.bool)
    kmask2 =  np.zeros((jpk,jpj,jpi),dtype=np.bool)
    for i in range(jpk):
        kmask1[i,:,:] = kmask1_2D
        kmask2[i,:,:] = kmask2_2D

# Coastness must be defined one by one
COASTNESS_LIST=[ 'open_sea']
    
COASTNESS = np.ones((jpk,jpj,jpi) ,dtype=[(coast,np.bool) for coast in COASTNESS_LIST])
COASTNESS['open_sea']  =  mask200_3D;

#DEPTH1=np.array([00, 050, 100, 150, 200, 0500, 1000, 1500, 2000, 2500, 3000, 3500, 4000])
Bottom_list=np.array([50, 100, 150, 200, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500])

nDepths = len(Bottom_list)
DEPTHlist      =['depth%02d' %(i) for i in range(nDepths)]

DEPTH  = np.zeros((jpk,jpj,jpi),dtype=[(depth,np.bool) for depth in DEPTHlist])
tk_top = 0
for idepth, depth in enumerate(DEPTHlist):
    tk_bottom = TheMask.getDepthIndex(Bottom_list[idepth])+1
    DEPTH[depth][tk_top:tk_bottom ,:,:] = True
    tk_top = tk_bottom


# tk_1     = TheMask.getDepthIndex(200.0)+1
# tk_2     = TheMask.getDepthIndex(600.0)+1
# 
# DEPTH['shallow'][0:tk_1   ,:,:] = True
# DEPTH['mid'    ][tk_1:tk_2,:,:] = True
# DEPTH['deep'   ][tk_2:    ,:,:] = True




Volume=np.zeros((jpk,jpj,jpi),dtype=np.double)
dZ     =np.ones ((jpk,jpj,jpi),dtype=np.double)
for i in range(jpk):
    Volume[i,:,:] = area*e3t[i]
    dZ[i,:,:]     = e3t[i]

L = SubMask.from_square_cutting(TheMask,1,-8.5, 29.5)
SUBlist=[ sub.name for sub in L ]

def SUB(sub):
    ''' sub is a string'''
    index= SUBlist.index(sub)
    basin = L[index]
    s=SubMask(basin,maskobject = TheMask)
    return s.mask



# SUB[med] is not applied by aveScan. 
#If we want it we hav to apply to each subbasin


def read_Positions_for_Pointprofiles(filename):

    dtIN  = np.dtype([('Name','S20'), ('Lon',np.float32), ('Lat',np.float32)])
    dtOUT = np.dtype([('Name','S20'), ('Lon',np.float32), ('Lat',np.float32), ('i',np.int), ('j',np.int)])  
    MeasPoints=np.loadtxt(filename, dtype=dtIN, skiprows=1,ndmin=1)
    
    nMeas=MeasPoints.size
    MeasPoints_OUT=np.zeros((nMeas),dtype=dtOUT)
    MeasPoints_OUT['Name']= MeasPoints['Name']
    MeasPoints_OUT['Lon' ]= MeasPoints['Lon' ]
    MeasPoints_OUT['Lat' ]= MeasPoints['Lat' ]
    for k in xrange(nMeas):
        DIST = (Lon - MeasPoints['Lon'][k])**2 + (Lat - MeasPoints['Lat'][k])**2 
        ind=np.nonzero(DIST==DIST.min())# tuple  
        j = ind[0]
        i = ind[1]
        MeasPoints_OUT['i'][k] = i
        MeasPoints_OUT['j'][k] = j
    
    return MeasPoints_OUT