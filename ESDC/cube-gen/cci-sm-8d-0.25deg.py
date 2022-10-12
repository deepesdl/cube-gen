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
store = new_data_store('cciodp')

dataset = store.open_data(
    'esacci.SOILMOISTURE.day.L3S.SSMV.multi-sensor.multi-platform.COMBINED.05-2.r1', 
    variable_names=['sm'],
    time_range=["1979-01-01","2019-12-31"]
)

last_year = 2019
first_year = 1979

years = np.arange(first_year,last_year + 1)

def resample_weekly(ds,year):
    keep_attrs = ds.time.attrs
    ds = ds.sel(time=slice(f"{year}-01-01",f"{year+1}-01-01")).resample(time="8D").mean()    
    ds['time'] = ds.time + np.timedelta64(4,"D")
    ds.time.attrs = keep_attrs
    return ds

print("Resampling in time")
dataset_8d = [resample_weekly(dataset,year) for year in tqdm(years)]
dataset_8d = xr.concat(dataset_8d,dim="time")

print("Chunking")
dataset_8d = dataset_8d.chunk(dict(time=256,lat=128,lon=128))

print("Saving")
dataset_8d.to_zarr("/net/scratch/dmontero/CCI/cci-sm-8d-0.25deg-256x128x128.zarr")