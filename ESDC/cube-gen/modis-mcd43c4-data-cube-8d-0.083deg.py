import xarray as xr
import xesmf as xe
import numpy as np
from tqdm import tqdm
from datetime import datetime

print("Reading")
dataset = xr.open_zarr("/net/scratch/dmontero/MODIS/modis-mcd43c4-vis-8d-0.05deg-256x128x128.zarr")

new_lats=np.load("/net/home/dmontero/DeepESDL/black-sea-datacube/cube-gen/ESDC/cube-gen/lat.npy")
new_lons=np.load("/net/home/dmontero/DeepESDL/black-sea-datacube/cube-gen/ESDC/cube-gen/lon.npy")

print("Interpolating")
dataset = dataset.sel(time=slice("2000-03-01","2022-01-01")).interp(coords=dict(lat=new_lats,lon=new_lons),method="linear")
dataset = dataset.chunk(dict(time=-1,lat=128,lon=128))
dataset = dataset.interpolate_na(dim="time",fill_value="extrapolate")
dataset = dataset.chunk(dict(time=256,lat=128,lon=128))

print("Adding attributes")
dataset.attrs['date_modified'] = str(datetime.now())
dataset.attrs['time_coverage_end'] = str(dataset.time[-1].values)
dataset.attrs['time_coverage_start'] = str(dataset.time[0].values)
dataset.attrs['processing_steps'] = dataset.attrs['processing_steps'] + ['Downsampling to 0.083 deg with bilinear interpolation','Interpolating NA with linear interpolation']

dataset.attrs['geospatial_lat_max'] = float(dataset.lat.max().values)
dataset.attrs['geospatial_lat_min'] = float(dataset.lat.min().values)
dataset.attrs['geospatial_lon_max'] = float(dataset.lon.max().values)
dataset.attrs['geospatial_lon_min'] = float(dataset.lon.min().values)

dataset.attrs['geospatial_lat_resolution'] = 0.0833
dataset.attrs['geospatial_lon_resolution'] = 0.0833

print("Saving")
dataset.to_zarr("/net/scratch/dmontero/MODIS/modis-mcd43c4-vis-8d-0.083deg-512x128x128.zarr")