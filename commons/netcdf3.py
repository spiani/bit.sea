import scipy.io.netcdf as NC
import os

def read_2d_file(filename,varname):
    ncIN = NC.netcdf_file(filename,'r')
    M2d = ncIN.variables[varname].data.copy()
    ncIN.close()
    return M2d

def write_2d_file(M2d,varname,outfile,mask,fillValue=1.e+20):
    ncOUT = NC.netcdf_file(outfile,'w')
    _, jpj, jpi= mask.shape
    ncOUT.createDimension("longitude", jpi)
    ncOUT.createDimension("latitude", jpj)
    ncvar = ncOUT.createVariable(varname, 'f', ('latitude','longitude'))
    setattr(ncvar,'fillValue'    ,fillValue)
    setattr(ncvar,'missing_value',fillValue)
    ncvar[:] = M2d
    ncOUT.close()
    
def write_3d_file(M3d,varname,outfile,mask,fillValue=1.e+20):
    '''
    Dumps a 3D array in a NetCDF file.
    
    
    Arguments
    * M3d       * the 3D array to dump
    * varname   * the variable name on NetCDF file
    * outfile   * file that will be created. If it is an existing file, 
                  it will be opened in 'append' mode.
    * mask      * a mask object consistent with M3d array
    * fillvalue * (optional) value to set missing_value attribute.
    
    Does not return anything.
    '''
    
    if os.path.exists(outfile):
        ncOUT=NC.netcdf_file(outfile,'a')
        print "appending ", varname, " in ", outfile
    else:
        ncOUT = NC.netcdf_file(outfile,'w')
        jpk, jpj, jpi= mask.shape
        ncOUT.createDimension("longitude", jpi)
        ncOUT.createDimension("latitude", jpj)
        ncOUT.createDimension("depth"   , jpk)
        
    ncvar = ncOUT.createVariable(varname, 'f', ('depth','latitude','longitude'))
    setattr(ncvar,'fillValue'    ,fillValue)
    setattr(ncvar,'missing_value',fillValue)
    ncvar[:] = M3d
    ncOUT.close()