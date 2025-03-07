import datetime
import glob
import os

import numpy as np
import xarray as xr
from tqdm import tqdm

pathIn = "~/data/SIF/GOSIF/source"
pathIn = os.path.expanduser(pathIn)

files = glob.glob(f"{pathIn}/*.tif")
files.sort()


def to_xarray(file):
    filename = file.split("/")[-1]
    date_info = filename.split("_", 1)[1].split(".")[0]
    date = np.datetime64(datetime.datetime.strptime(date_info, '%Y%j'))
    ds = xr.open_dataset(file, engine="rasterio",
                         chunks={"x": 1024, "y": 1024}).where(
        lambda x: x < 32766, other=np.nan)
    ds = ds.reset_coords().band_data.sel(band=1).drop("band").rename(
        {"y": "lat", "x": "lon"})
    ds.name = "sif"
    ds = ds.to_dataset()
    ds = ds.assign_coords({"time": date}).expand_dims("time")
    ds = ds * 0.0001
    ds = ds.transpose("time", "lat", "lon")
    ds.to_zarr(f"{pathIn}/{filename.replace('.tif', '.zarr')}")


[to_xarray(file) for file in tqdm(files)]
