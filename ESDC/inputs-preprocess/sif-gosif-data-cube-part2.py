import xarray as xr
import numpy as np
import glob
import os
import datetime
from tqdm import tqdm

pathOut = "/net/projects/deep_esdl/data/GOSIF/cubes/"

if not os.path.exists(pathOut):
    os.mkdir(pathOut)
    
files = glob.glob("/net/projects/deep_esdl/data/GOSIF/data/*.zarr")
files.sort()

ref = xr.open_zarr(files[0])

datasets = []

for file in tqdm(files):
    ds = xr.open_zarr(file)
    ds["lon"] = ref.lon
    datasets.append(ds)
    
datasets = xr.concat(datasets,dim = "time")

datasets.to_zarr(f"{pathOut}/sif-gosif-no-metadata-1x1024x1024.zarr")