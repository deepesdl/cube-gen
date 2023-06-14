import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os
from datetime import datetime, timedelta
import pandas as pd

pathIn = f"~/data/hydrology/source/SWE_CPC_GPM_ERA5downT_RadGhent_filter5mm/"
pathIn = os.path.expanduser(pathIn)

files = glob(f"{pathIn}/*.nc")
files.sort()

for file in tqdm(files):
    filename = file.split("/")[-1].replace(".nc",".zarr")
    if not os.path.exists(f"{pathIn}{filename}"):
        ds = xr.open_dataset(file)
        ds = ds.rename(dict(t="time",Y="lat",X="lon"))
        ds["time"] = pd.to_datetime(ds.Time.values-719529, unit='d').values
        ds["lat"] = ds.Lat[:,0]
        ds["lon"] = ds.Lon[0,:]
        ds = ds.drop(["Lon","Lat","Time"])
        ds = ds.chunk(dict(time=-1,lon=64,lat=64))
        ds.to_zarr(f"{pathIn}{filename}")