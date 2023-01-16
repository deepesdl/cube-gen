import xarray as xr
import numpy as np
import rioxarray
import geopandas as gpd
import os
from glob import glob

def regrid(filepath):
    
    da = xr.open_dataset(filepath)
    
    x = np.arange(da.x_range[0],da.x_range[1],da.spacing[0].values)
    y = np.arange(da.y_range[0],da.y_range[1],da.spacing[1].values)
    z = np.reshape(da.z.values,(da.dimension[1].values,da.dimension[0].values))
    
    da = xr.DataArray(
        data=z,
        dims=["y", "x"],
        coords=dict(
            y=("y", y),
            x=("x", x),
        ),
    )
    
    return da

for size in [200,300]:

    pathIn = f"~/data/polar/source/curie_depth_estimates_{size}x{size}km_xyz_data"
    pathIn = os.path.expanduser(pathIn)

    pathOut = f"~/data/polar/cubes/curie_depth_estimates_{size}x{size}km_xyz_data"
    pathOut = os.path.expanduser(pathOut)

    if not os.path.exists(pathOut):
        os.makedirs(pathOut)

    filepath = os.path.join(pathIn,f'{size}km_Dziadek_etal_CurieDepth_Results.nc')

    da = regrid(filepath)

    da.name = f"curie_depth_{size}km"

    da = da.to_dataset()
    da = da.chunk()

    da.to_zarr(f"{pathOut}/curie_depth_{size}km.zarr")