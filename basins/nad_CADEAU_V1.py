from os import path,listdir
import re
from basins.region import Polygon
from basins.basin import SimplePolygonalBasin, ComposedBasin
import numpy as np

currentdir=path.dirname(path.realpath(__file__))
datadir=path.join(currentdir,'NAD_CADEAU_DATA')

zones=[]
zone_list=[]

#adr2 = Polygon([ 14.0,20.0,20,18.5,18.0,16.6,13.0],
#               [ 42.5,42.5,40,40.0,40.5,41.0,42.5])
#adr2 = SimplePolygonalBasin('adr2', adr2,'Southern Adriatic')
#basin_001.txt
for  f in sorted(listdir(datadir)):
    fmask='basin_(?P<index>[0-9][0-9][0-9]).txt'
    fmatch=re.match(fmask,f)
    if fmatch is None:
       continue
    zone_index=int(fmatch.group('index'))
    filein=datadir+'/'+f
    lonlat=np.loadtxt(filein)

    zone_name='zone_' + str(zone_index).zfill(3)

    zone=Polygon(lonlat[0,:],lonlat[1,:])

    zones.append(SimplePolygonalBasin(zone_name,zone,zone_name))

#
P   = ComposedBasin('P',zones)
