import glob
import os

import xarray as xr
from tqdm import tqdm

pathIn = "~/data/SIF/GOSIF/source"
pathIn = os.path.expanduser(pathIn)

pathOut = "~/data/SIF/GOSIF/preprocess"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)

files = glob.glob(f"{pathIn}/*.zarr")
files.sort()

ref = xr.open_zarr(files[0])

datasets = []

for file in tqdm(files):
    ds = xr.open_zarr(file)
    ds["lon"] = ref.lon
    datasets.append(ds)

datasets = xr.concat(datasets, dim="time")

datacube = xr.open_zarr(f"{pathIn}/sif-gosif-1x1024x1024.zarr")
