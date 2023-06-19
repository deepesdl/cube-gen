import glob
import os

import numpy as np
import xarray as xr
from tqdm import tqdm

pathOut = "~/data/CCI/sm/preprocess"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)

pathIn = "~/data/CCI/sm/source"
pathIn = os.path.expanduser(pathIn)

print("Reading")
files = glob.glob(f"{pathIn}/*.zarr")
files.sort()

dataset = [xr.open_zarr(file) for file in tqdm(files)]
dataset = xr.concat(dataset, dim="time")
dataset = dataset.chunk(dict(time=256))

last_year = 2020
first_year = 1979

years = np.arange(first_year, last_year + 1)


def resample_weekly(ds, year):
    keep_attrs = ds.time.attrs
    ds = ds.sel(time=slice(f"{year}-01-01", f"{year + 1}-01-01")).resample(
        time="8D").mean()
    ds['time'] = ds.time + np.timedelta64(4, "D")
    ds.time.attrs = keep_attrs
    return ds


print("Resampling in time")
dataset_8d = [resample_weekly(dataset, year) for year in tqdm(years)]
dataset_8d = xr.concat(dataset_8d, dim="time")
dataset_8d = dataset_8d.chunk(dict(time=256))

print("Saving")
dataset_8d.to_zarr(f"{pathOut}/cci-sm-8d-0.25deg-256x128x128.zarr")
