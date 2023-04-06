import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os

pathIn = f"~/data/ocean/source/monthly_global_phytoplankton_carbon/"
pathIn = os.path.expanduser(pathIn)

files = glob(f"{pathIn}/*.nc")
files.sort()

for file in tqdm(files):
    filename = file.split("/")[-1].replace(".nc",".zarr")
    if not os.path.exists(f"{pathIn}{filename}"):
        try:
            ds = xr.open_dataset(file)
            ds = ds.astype("float32")
            ds['lat'] = ds.latitude.values
            ds['lon'] = ds.longitude.values
            if ("latitude" in ds.variables) and ("longitude" in ds.variables):
                ds = ds.drop(["latitude","longitude"])
            ds['time'] = ds.time.astype('datetime64[M]').astype('datetime64[ns]')
            ds = ds.chunk(dict(time=1,lon=256,lat=256))
            ds.to_zarr(f"{pathIn}{filename}")
        except:
            pass