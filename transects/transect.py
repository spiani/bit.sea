# Copyright (c) 2015 eXact Lab srl
# Author: Gianfranco Gallizia <gianfranco.gallizia@exact-lab.it>
import numpy as np
from xml.dom import minidom
from ast import literal_eval
from commons.segment import Segment
from commons.helpers import is_number
from commons.xml import *
from commons.mask import Mask
from commons.dataextractor import DataExtractor

class Transect(object):
    """Stores a multiple segment transect definition.
    """
    def __init__(self, varname, clim, segmentlist):
        """Transect constructor.

        Args:
            - *varname*: the name of the variable to extract.
            - *clim*: a list or tuple with the two limit values (minimum and
              maximum)
            - *segmentlist*: a list Segment objects. Can be an empty list.
        """
        self.__varname = str(varname)
        if not isinstance(clim, (list, tuple)) or (len(clim) != 2) or not (is_number(clim[0]) and is_number(clim[1])):
            raise ValueError("clim must be a list of two numbers")
        self.__clim = clim
        if not isinstance(segmentlist, (list, tuple)) or ((len(segmentlist) > 0) and not isinstance(segmentlist[0], (Segment,))):
            raise ValueError("segmentlist must be a list of Segments")
        self.__segmentlist = segmentlist
        #Variable data cache
        self.__datacache = { 'filename':None, 'data':None }

    @property
    def varname(self):
        return self.__varname

    @property
    def clim(self):
        return self.__clim

    @property
    def segmentlist(self):
        return self.__segmentlist

    def get_transect_data(self, segment_index, mask, datafilepath, fill_value=np.nan, timestep=0):
        """Extracts transect data from a NetCDF file.

        Args:
            - *segment_index*: the index of the segment to retrieve.
            - *mask*: a commons.Mask object.
            - *datafilepath*: path to the NetCDF data file.
            - *fill_value* (optional): value to use when there's no data
              available (default: np.nan).
            - *timestep* (optional): the time index (default: 0).
        Returns: a NumPy array that contains the requested data.
        """
        #Input validation
        if not is_number(segment_index):
            raise ValueError("'%s' is not a number." % (segment_index,))
        seg = self.__segmentlist[segment_index]
        if not isinstance(mask, (Mask,)):
            raise ValueError("mask must be a Mask object.")
        datafilepath = str(datafilepath)
        #Retrieve indices
        x_min, y_min = mask.convert_lon_lat_to_indices(seg.lon_min, seg.lat_min)
        x_max, y_max = mask.convert_lon_lat_to_indices(seg.lon_max, seg.lat_max)
        #Check if we don't have cached data
        if (self.__datacache['filename'] is None) or (self.__datacache['filename'] != datafilepath):
            #Read data from the NetCDF file
            de = DataExtractor(self.__varname, datafilepath, mask, fill_value)
            self.__datacache['filename'] = datafilepath
            self.__datacache['data'] = de.filled_values
        #Check for single point case
        if (x_min == x_max) and (y_min == y_max):
            raise ValueError("Invalid segment: %s" % (seg,))
        #Get the output data
        if x_min == x_max:
            data = np.array(self.__datacache['data'][timestep,:,y_min:y_max,x_min], dtype=float)
        elif y_min == y_max:
            data = np.array(self.__datacache['data'][timestep,:,y_min,x_min:x_max], dtype=float)
        else:
            raise ValueError("Invalid segment: %s" % (seg,))
        return data

    @staticmethod
    def get_list_from_XML_file(plotlistfile):
        xmldoc = minidom.parse(plotlistfile)
        output = list()
        #For each Transects element
        for t in xmldoc.getElementsByTagName("Transects"):
            #Build the segment list
            segmentlist = list()
            for sdef in get_subelements(t, "transect"):
                lon_min = literal_eval(get_node_attr(sdef, "lonmin"))
                lat_min = literal_eval(get_node_attr(sdef, "latmin"))
                lon_max = literal_eval(get_node_attr(sdef, "lonmax"))
                lat_max = literal_eval(get_node_attr(sdef, "latmax"))
                if (lon_min != lon_max) and (lat_min != lat_max):
                    raise NotImplementedError("You have to fix a coordinate. Either Longitude or Latitude.")
                segmentlist.append(Segment((lon_min, lat_min),(lon_max, lat_max)))
            #For each vars list
            for vl in get_subelements(t, "vars"):
                for v in get_subelements(vl, "var"):
                    varname = get_node_attr(v, "name")
                    clim = literal_eval(get_node_attr(v, "clim"))
                    output.append(Transect(varname, clim, segmentlist))
        return output