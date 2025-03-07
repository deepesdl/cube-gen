import os

import numpy as np
import xarray as xr

pathOut = "~/data/CCI/sm/preprocess"
pathOut = os.path.expanduser(pathOut)

print("Reading")
dataset_8d = xr.open_zarr(f"{pathOut}/cci-sm-8d-0.25deg-256x128x128.zarr")
new_lats = np.load("lat.npy")
new_lons = np.load("lon.npy")

print("Resampling in space")
dataset_8d = dataset_8d.interp(coords=dict(lat=new_lats, lon=new_lons),
                               method="nearest")
dataset_8d = dataset_8d.chunk(dict(time=256, lat=128, lon=128))

print("Saving")
dataset_8d.to_zarr(f"{pathOut}/cci-sm-8d-0.083deg-256x128x128.zarr")
