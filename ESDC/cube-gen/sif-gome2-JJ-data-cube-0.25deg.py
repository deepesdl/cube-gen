import xarray as xr
import xesmf as xe
import numpy as np
from tqdm import tqdm
from datetime import datetime

print("Reading")
dataset = xr.open_zarr("/net/data/SIF/sif-gome2-JJ-256x256x256.zarr")

print("Interpolating")
dataset = dataset.coarsen(lat=5,lon=5).mean()
dataset = dataset.chunk(dict(time=-1,lat=64,lon=64))
dataset = dataset.interpolate_na(dim="time",fill_value="extrapolate")
dataset = dataset.chunk(dict(time=256,lat=128,lon=128))

print("Adding attributes")
dataset.attrs['date_modified'] = str(datetime.now())
dataset.attrs['time_coverage_end'] = str(dataset.time[-1].values)
dataset.attrs['time_coverage_start'] = str(dataset.time[0].values)
dataset.attrs['processing_steps'] = dataset.attrs['processing_steps'] + ['Downsampling to 0.25 deg with mean','Interpolating NA with linear interpolation']

dataset.attrs['geospatial_lat_max'] = float(dataset.lat.max().values)
dataset.attrs['geospatial_lat_min'] = float(dataset.lat.min().values)
dataset.attrs['geospatial_lon_max'] = float(dataset.lon.max().values)
dataset.attrs['geospatial_lon_min'] = float(dataset.lon.min().values)

dataset.attrs['geospatial_lat_resolution'] = 0.25
dataset.attrs['geospatial_lon_resolution'] = 0.25

print("Saving")
dataset.to_zarr("/net/scratch/dmontero/SIF/sif-gome2-JJ-8d-0.25deg-256x128x128.zarr")