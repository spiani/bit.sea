# Copyright (c) 2015 eXact Lab srl
# Author: Gianfranco Gallizia <gianfranco.gallizia@exact-lab.it>
import numpy as np
import netCDF4

class Mask(object):
    """
    Defines a mask from a NetCDF file
    """
    def __init__(self, filename, maskvarname="tmask", zlevelsvar="nav_lev"):
        filename = str(filename)
        try:
            dset = netCDF4.Dataset(filename)
            if maskvarname in dset.variables:
                m = dset.variables[maskvarname]
                if len(m.shape) == 4:
                    self.__mask = np.array(m[0,:,:,:], dtype=np.bool)
                elif len(m.shape) == 3:
                    self.__mask = np.array(m[:,:,:], dtype=np.bool)
                else:
                    raise ValueError("Wrong shape: %s" % (m.shape,))
                self.__shape = self.__mask.shape
            else:
                raise ValueError("maskvarname '%s' not found" % (str(maskvarname),))
            if zlevelsvar in dset.variables:
                z = dset.variables[zlevelsvar]
                if len(z.shape) != 1:
                    raise ValueError("zlevelsvar must have only one dimension")
                if not z.shape[0] in self.__shape:
                    raise ValueError("cannot match %s lenght with any of %s dimensions" % (zlevelsvar, maskvarname))
                self.__zlevels = np.array(dset.variables[zlevelsvar])
            else:
                raise ValueError("zlevelsvar '%s' not found" % (str(zlevelsvar),))
        except:
            raise

    @property
    def mask(self):
        return self.__mask

    @property
    def zlevels(self):
        return self.__zlevels

    @property
    def shape(self):
        return self.__shape