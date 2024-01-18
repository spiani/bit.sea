from commons.mask import Mask, MaskBathymetry
from nad_CADEAU_V1 import P
import numpy as np

mask = Mask('/g100/home/userexternal/plazzari/my_scripts/NORTH_ADRIATIC/meshmask_total.nc')
#mask = Mask('../../masks_NARF/meshmask_006_014.nc')
mask_bathymetry = MaskBathymetry.build_bathymetry(mask)

bathymetry = mask_bathymetry

def plot_basins():
    import matplotlib.pyplot as plt
    import cartopy
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    from matplotlib.backends.backend_pdf import PdfPages

    basins = P.basin_list#generate_basins_for_adriatic(bathymetry)

    # colors = ["blue", "green", "gold", "pink", "red", "orange", "olive", "purple", "cyan"]
    cmap = plt.get_cmap('nipy_spectral')
    plt.figure(dpi=300)
    axes = plt.axes(projection=ccrs.PlateCarree())

    for i, basin in enumerate(basins):
        title = basin.name
        print(title)
        basin.plot(color=cmap(float(i) / (len(basins))), alpha=.75, lon_window=(12, 16), lat_window=(43, 46), lon_points=1000, lat_points=1000, axes=axes)
    
    land = cfeature.NaturalEarthFeature(
        category='physical',
        name='land',
        scale='10m',
        facecolor=(0.5, 0.5, 0.5, 0.8))
    axes.add_feature(land, zorder=2)
    plt.savefig('NAD_V1.png')

plot_basins()
