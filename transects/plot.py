# Copyright (c) 2016 eXact Lab srl
# Author: Gianfranco Gallizia <gianfranco.gallizia@exact-lab.it>
# Transect plotting routines

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def decimate(a, how_many):
    #selector = np.mod(np.array(range(len(a))),len(a)/how_many) == 0
    indices = np.linspace(0, len(a)-1, how_many)
    data = list()
    for i in indices:
        data.append(a[i])
    return np.array(data), indices

def transectplot(transect, segment, date, segmentdata=None, fig=None, ax=None, dpi=72.0, cbar_ticks=5, h_ticks=8, z_ticks=7):
    #Check if segment is in transect.segmentlist
    if segment in transect.segmentlist:
        index = transect.segmentlist.index(segment)
        if segmentdata is None:
            segmentdata = transect.get_segment_data()
        data = segmentdata[index]['data']
        h_vals, h_in = decimate(segmentdata[index]['h_vals'], h_ticks)
        h_vals = np.around(h_vals, decimals=2)
        z_vals, z_in = decimate(segmentdata[index]['z_vals'], z_ticks)
        z_vals = np.around(z_vals)
        shape = data.shape
    else:
        raise ValueError("Segment %s not found among transect segments." % repr(segment))
    #If the user has not passed existing figure and axes create them
    if (fig is None) or (ax is None):
        fig , ax = plt.subplots()
        fig.set_dpi(dpi)
        fig.set_size_inches(shape[1] / float(dpi), shape[0] / float(dpi))
    else:
        #Clear the figure before plotting
        fig.clf()
        fig.add_axes(ax)
    #Set color limits
    clim = transect.clim
    #Plot the data
    im = ax.imshow(data)
    #Set color bar
    im.set_clim(clim[0], clim[1])
    cbar_ticks_list = np.linspace(clim[0], clim[1], cbar_ticks).tolist()
    cbar_ticks_labels = list()
    for t in cbar_ticks_list:
        cbar_ticks_labels.append("%g" % (t,))
    div = make_axes_locatable(ax)
    cax = div.append_axes("right", size="3%", pad=0.05)
    cbar = fig.colorbar(im, cax=cax, ticks=cbar_ticks_list)
    cbar.ax.set_yticklabels(cbar_ticks_labels)
    #Set X axis ticks
    ax.set_xticks(h_in)
    ax.set_xticklabels(h_vals)
    #Set Y axis ticks
    ax.set_yticks(z_in)
    ax.set_yticklabels(z_vals)
    #Add title to figure
    title = "%s %s %s" % (date, segment.name, transect.varname)
    fig.suptitle(title)
    return segmentdata, fig, ax