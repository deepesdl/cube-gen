import xarray as xr
import numpy as np
import spyndex
import glob
import os
import datetime
from tqdm import tqdm

before = datetime.datetime.now()

mcd43c4 = xr.open_zarr("/net/projects/deep_esdl/data/MODIS/MCD43C4/cubes/modis-mcd43c4-no-metadata-256x256x256.zarr")
ndvi = xr.open_zarr("/net/projects/deep_esdl/data/MODIS/MCD43C4/cubes/modis-mcd43c4-ndvi-no-metadata-256x256x256.zarr")
nirv = xr.open_zarr("/net/projects/deep_esdl/data/MODIS/MCD43C4/cubes/modis-mcd43c4-nirv-no-metadata-256x256x256.zarr")
kndvi = xr.open_zarr("/net/projects/deep_esdl/data/MODIS/MCD43C4/cubes/modis-mcd43c4-kndvi-no-metadata-256x256x256.zarr")

print("Merging datasets")

datasets = xr.merge([mcd43c4,ndvi,nirv,kndvi])

print("Saving...")
    
datasets.to_zarr(f"/net/projects/deep_esdl/data/MODIS/MCD43C4/cubes/modis-mcd43c4-vis-no-metadata-256x256x256.zarr")

print("Done!")
print(f"Everything took {((datetime.datetime.now() - before).total_seconds())/60} minutes in total")