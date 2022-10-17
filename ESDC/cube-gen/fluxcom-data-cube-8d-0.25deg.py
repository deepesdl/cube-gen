import xarray as xr
import numpy as np
from tqdm import tqdm
from datetime import datetime

print("Reading")
dataset = xr.open_zarr("/Net/Groups/BGI/work_1/scratch/dmontero/FLUXCOM/metadata/fluxcom-8d-0.083deg-256x256x256.zarr")

print("Interpolating")
dataset = dataset.coarsen(lat=3,lon=3).mean()
dataset = dataset.chunk(dict(time=256,lat=128,lon=128))

print("Adding attributes")
dataset.attrs['date_modified'] = str(datetime.now())
dataset.attrs['time_coverage_end'] = str(dataset.time[-1].values)
dataset.attrs['time_coverage_start'] = str(dataset.time[0].values)
dataset.attrs['processing_steps'] = dataset.attrs['processing_steps'] + ['Downsampling to 0.25 deg with mean']

dataset.attrs['geospatial_lat_max'] = float(dataset.lat.max().values)
dataset.attrs['geospatial_lat_min'] = float(dataset.lat.min().values)
dataset.attrs['geospatial_lon_max'] = float(dataset.lon.max().values)
dataset.attrs['geospatial_lon_min'] = float(dataset.lon.min().values)

dataset.attrs['geospatial_lat_resolution'] = 0.25
dataset.attrs['geospatial_lon_resolution'] = 0.25

for variable in dataset.variables.keys():
    del dataset[variable].encoding['chunks']

print("Saving")
dataset.to_zarr("/Net/Groups/BGI/work_1/scratch/dmontero/FLUXCOM/metadata/fluxcom-8d-0.25deg-256x128x128.zarr")