from commons.mask import Mask, MaskBathymetry
from nad_V0 import generate_basins_for_adriatic
import cv2 as cv
import numpy as np

mask = Mask('/g100/home/userexternal/plazzari/my_scripts/NORTH_ADRIATIC/meshmask_total.nc')
#mask = Mask('../../masks_NARF/meshmask_006_014.nc')
mask_bathymetry = MaskBathymetry.build_bathymetry(mask)

bathymetry = mask_bathymetry

def plot_basins():
    import matplotlib.pyplot as plt
#   import cartopy
#   import cartopy.crs as ccrs
#   import cartopy.feature as cfeature
    from matplotlib.backends.backend_pdf import PdfPages

    basins = generate_basins_for_adriatic(bathymetry)

    # colors = ["blue", "green", "gold", "pink", "red", "orange", "olive", "purple", "cyan"]
    cmap = plt.get_cmap('nipy_spectral')
    with PdfPages('prova01_countours.pdf') as pdf:
        plt.figure(dpi=1200)
        axes = plt.gca()

        for i, basin in enumerate(basins[0:3]):
            title = basin.name
            print(title)
            lon,lat,data=basin.plot(color=cmap(float(i) / (len(basins))), alpha=.75, lon_window=(12, 16), lat_window=(43, 46), lon_points=1000, lat_points=1000, axes=axes)
            tableau_poche = data.astype(np.uint8)
            contours, hierarchy = cv.findContours(tableau_poche, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

            npoints=0
            for ncon in range(len(contours)):
                npoints_test=contours[ncon][:,0,0].shape[0]
                if npoints_test > npoints:
                    x=contours[ncon][:,0,0]
                    y=contours[ncon][:,0,1]
                    npoints=npoints_test

            print(f'    zone_{i}_lon = {lon[x]}')
            print(f'    zone_{i}_lat = {lat[y]}')
            print("        ")
            plt.pcolor(data)
            plt.plot(x,y)
            pdf.savefig()
            plt.close()
    
#   land = cfeature.NaturalEarthFeature(
#       category='physical',
#       name='land',
#       scale='10m',
#       facecolor=(0.5, 0.5, 0.5, 0.8))
#   axes.add_feature(land, zorder=2)
    plt.savefig('prova_with_rivers.pdf')

plot_basins()
