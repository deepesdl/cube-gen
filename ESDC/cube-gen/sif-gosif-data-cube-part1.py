import xarray as xr
import numpy as np
import glob
import os
import datetime
from tqdm import tqdm

pathOut = "/net/projects/deep_esdl/data/GOSIF/cubes/"

if not os.path.exists(pathOut):
    os.mkdir(pathOut)
    
files = glob.glob("/net/projects/deep_esdl/data/GOSIF/data/*.tif")
files.sort()

def to_xarray(file):
    filename = file.split("/")[-1]
    date = np.datetime64(datetime.datetime.strptime(filename[6:13],'%Y%j'))
    ds = xr.open_dataset(file,engine = "rasterio",chunks = {"x":1024,"y":1024}).where(lambda x: x < 32766,other = np.nan)
    ds = ds.reset_coords().band_data.sel(band = 1).drop("band").rename({"y": "lat", "x":"lon"})
    ds.name = "sif"
    ds = ds.to_dataset()
    ds = ds.assign_coords({"time": date}).expand_dims("time")
    ds = ds * 0.0001
    ds = ds.transpose("time","lat","lon")
    ds.to_zarr(f"/net/projects/deep_esdl/data/GOSIF/data/{filename.replace('.tif','.zarr')}")

[to_xarray(file) for file in tqdm(files)]