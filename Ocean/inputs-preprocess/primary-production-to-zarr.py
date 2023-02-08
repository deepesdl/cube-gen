import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os

pathIn = f"~/data/ocean/source/monthly_global_marine_phytoplankton_primary_production/"
pathIn = os.path.expanduser(pathIn)

files = glob(f"{pathIn}/*.nc")
files.sort()

for file in tqdm(files):
    filename = file.split("/")[-1].replace(".nc",".zarr")
    ds = xr.open_dataset(file)
    ds = ds.astype("float32")
    if ("latitude" in ds.variables) and ("longitude" in ds.variables):
        ds = ds.drop(["latitude","longitude"])
    ds['time'] = ds.time.astype('datetime64[M]')
    ds = ds.chunk(dict(time=1,lon=256,lat=256))
    ds.to_zarr(f"{pathIn}{filename}")