from commons.mask import Mask, MaskBathymetry
from nad_V0 import generate_basins_for_adriatic

mask = Mask('../../masks_NARF/meshmask.nc')
#mask = Mask('../../masks_NARF/meshmask_006_014.nc')
mask_bathymetry = MaskBathymetry.build_bathymetry(mask)

bathymetry = mask_bathymetry

def plot_basins():
    import matplotlib.pyplot as plt
#   import cartopy
#   import cartopy.crs as ccrs

    basins = generate_basins_for_adriatic(bathymetry)

    colors = ["blue", "green", "gold", "pink", "red", "orange", "olive", "purple", "cyan"]

    plt.figure(dpi=1200)
    axes = plt.gca()
#   axes = plt.axes(projection=ccrs.PlateCarree())
    for i, basin in enumerate(basins):
        title = basin.name
        print(title)
        basin.plot(color=colors[i % len(colors)], alpha=.75, lon_window=(9, 21), lat_window=(37, 47), lon_points=500, lat_points=500, axes=axes)

#   axes.coastlines()
#   axes.add_feature(cartopy.feature.LAND, facecolor=(0.5,0.5,0.5, 0.8), zorder=2)
    plt.savefig('prova02.pdf')

plot_basins()
