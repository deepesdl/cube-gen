import os
from datetime import datetime

import numpy as np
import xarray as xr

pathOut = "~/data/SIF/GOSIF/output"
pathOut = os.path.expanduser(pathOut)

print("Reading")
dataset = xr.open_zarr(f"{pathOut}/sif-gosif-8d-0.05deg-1x1024x1024.zarr")

print("Fixing time")
keep_attrs = dataset.time.attrs
dataset["time"] = dataset.time + np.timedelta64(4, "D")
dataset.time.attrs = keep_attrs

print("Coarsing")
dataset = dataset.coarsen(lat=5, lon=5).mean()

print("Chunking")
dataset = dataset.chunk(dict(time=256, lat=128, lon=128))

print("Adding attrs")
dataset.attrs['date_modified'] = str(datetime.now())
dataset.attrs['time_coverage_end'] = str(dataset.time[-1].values)
dataset.attrs['time_coverage_start'] = str(dataset.time[0].values)
dataset.attrs['reported_day'] = 5.0
dataset.attrs['processing_steps'] = dataset.attrs['processing_steps'] + [
    'Downsampling to 0.25 deg with mean']

dataset.attrs['geospatial_lat_max'] = float(dataset.lat.max().values)
dataset.attrs['geospatial_lat_min'] = float(dataset.lat.min().values)
dataset.attrs['geospatial_lon_max'] = float(dataset.lon.max().values)
dataset.attrs['geospatial_lon_min'] = float(dataset.lon.min().values)

dataset.attrs['geospatial_lat_resolution'] = 0.25
dataset.attrs['geospatial_lon_resolution'] = 0.25

print("Deleting previous chunks")
del dataset['sif'].encoding['chunks']

print("Saving")
dataset.to_zarr(f"{pathOut}/sif-gosif-8d-0.25deg-256x128x128.zarr")
