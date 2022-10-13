import numpy as np
from tqdm import tqdm
import xarray as xr
import glob

print("Reading")
files = glob.glob("/net/scratch/dmontero/CCI/SM/*.zarr")
files.sort()

dataset = [xr.open_zarr(file) for file in tqdm(files)]
dataset = xr.concat(dataset,dim="time")
dataset = dataset.chunk(dict(time=256))

last_year = 2020
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
dataset = dataset.chunk(dict(time=256))

print("Saving")
dataset_8d.to_zarr("/net/scratch/dmontero/CCI/cci-sm-8d-0.25deg-256x128x128.zarr")