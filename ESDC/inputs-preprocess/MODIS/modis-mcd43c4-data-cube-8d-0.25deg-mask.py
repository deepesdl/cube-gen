import xarray as xr
import xesmf as xe
import numpy as np
from tqdm import tqdm
from datetime import datetime

pathGLEAM = "~/data/GLEAM/output"
pathGLEAM = os.path.expanduser(pathGLEAM)

pathOut = "~/data/MODIS/output"
pathOut = os.path.expanduser(pathOut)

print("Reading")
dataset = xr.open_zarr(f"{pathOut}/modis-mcd43c4-vis-8d-0.25deg-256x128x128.zarr")

mask = xr.open_zarr(f"{pathGLEAM}/gleam-8d-0.25deg-256x128x128.zarr")
mask = (mask.SMsurf[0]/mask.SMsurf[0]).drop("time")

mask["lat"] = dataset.lat
mask["lon"] = dataset.lon

print("Masking")
masked = (mask * dataset)

print("Adding attrs")
for variable in list(masked.variables):
    masked[variable].attrs = dataset[variable].attrs
    
masked.attrs = dataset.attrs

masked.attrs['date_modified'] = str(datetime.now())
masked.attrs['processing_steps'] = masked.attrs['processing_steps'] + ['Masking water using GLEAM as reference']

masked = masked.transpose("time","lat","lon")

print("Saving")
masked.to_zarr(f"{pathOut}/modis-mcd43c4-vis-mask-8d-0.25deg-256x128x128.zarr")