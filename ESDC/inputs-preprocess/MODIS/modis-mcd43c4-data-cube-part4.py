import xarray as xr
import numpy as np
import spyndex
import glob
import os
import datetime
from tqdm import tqdm

before = datetime.datetime.now()

pathOut = "~/data/MODIS/preprocess"
pathOut = os.path.expanduser(pathOut)

mcd43c4 = xr.open_zarr(f"{pathOut}/modis-mcd43c4-256x256x256.zarr")
ndvi = xr.open_zarr(f"{pathOut}/modis-mcd43c4-ndvi-256x256x256.zarr")
nirv = xr.open_zarr(f"{pathOut}/modis-mcd43c4-nirv-256x256x256.zarr")
kndvi = xr.open_zarr(f"{pathOut}/modis-mcd43c4-kndvi-256x256x256.zarr")

print("Merging datasets")

datasets = xr.merge([mcd43c4,ndvi,nirv,kndvi])

print("Saving...")
    
datasets.to_zarr(f"{pathOut}/modis-mcd43c4-vis-256x256x256.zarr")

print("Done!")
print(f"Everything took {((datetime.datetime.now() - before).total_seconds())/60} minutes in total")