import xarray as xr
import numpy as np
import rioxarray
import geopandas as gpd
import os
from glob import glob

pathIn = "~/data/polar/source/magnetic_anomaly"
pathIn = os.path.expanduser(pathIn)

pathOut = "~/data/polar/cubes/magnetic_anomaly"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)
    
magnetic_path = os.path.join(pathIn,'ASE_MagneticCompilation_Dziadeketal_250m.tif')

def to_xarray(da):
    da = da.isel(band=0).drop("band")
    da.attrs = dict()
    da.name = "magnetic_anomaly"
    da = da.to_dataset()
    return da

magnetic = to_xarray(rioxarray.open_rasterio(magnetic_path))
magnetic = magnetic.chunk()

magnetic.to_zarr(f"{pathOut}/magnetic_anomaly.zarr")