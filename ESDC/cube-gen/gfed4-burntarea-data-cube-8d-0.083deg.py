from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

import shapely.geometry
from IPython.display import JSON
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import xarray as xr

print("Reading")
dataset_8d = xr.open_zarr("/net/scratch/dmontero/GFED4/cubes/gfed4-burntarea-8d-0.25deg-256x128x128.zarr")

new_lats = np.load("lat.npy")
new_lons = np.load("lon.npy")

print("Resampling in space")
dataset_8d = dataset_8d.interp(coords=dict(lat=new_lats,lon=new_lons),method="nearest")
dataset_8d = dataset_8d.chunk(dict(time=256,lat=128,lon=128))

print("Saving")
dataset_8d.to_zarr("/net/scratch/dmontero/GFED4/cubes/gfed4-burntarea-8d-0.083deg-256x128x128.zarr")
