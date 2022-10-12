import xarray as xr
import numpy as np
import spyndex
import glob
import os
import datetime
from tqdm import tqdm

before = datetime.datetime.now()

datasets = xr.open_zarr("/net/projects/deep_esdl/data/MODIS/MCD43C4/cubes/modis-mcd43c4-no-metadata-256x256x256.zarr")

print("Computing NDVI")

indices = spyndex.computeIndex(
    index = ["NDVI"],
    N = datasets.Nadir_Reflectance_Band2,
    R = datasets.Nadir_Reflectance_Band1
)

indices.name = "NDVI"
indices = indices.to_dataset()

indices.to_zarr(f"/net/projects/deep_esdl/data/MODIS/MCD43C4/cubes/modis-mcd43c4-ndvi-no-metadata-256x256x256.zarr")
print(f"NDVI took {((datetime.datetime.now() - before).total_seconds())/60} minutes in total")

print("Computing NIRv")

indices = spyndex.computeIndex(
    index = ["NIRv"],
    N = datasets.Nadir_Reflectance_Band2,
    R = datasets.Nadir_Reflectance_Band1
)

indices.name = "NIRv"
indices = indices.to_dataset()

indices.to_zarr(f"/net/projects/deep_esdl/data/MODIS/MCD43C4/cubes/modis-mcd43c4-nirv-no-metadata-256x256x256.zarr")
print(f"NDVI + NIRv took {((datetime.datetime.now() - before).total_seconds())/60} minutes in total")

print("Computing kNDVI")

indices = spyndex.computeIndex(
    index = ["kNDVI"],
    kNN = 1.0,
    kNR = spyndex.computeKernel(
        kernel = "RBF",
        a = datasets.Nadir_Reflectance_Band2,
        b = datasets.Nadir_Reflectance_Band1,
        sigma = (datasets.Nadir_Reflectance_Band2 + datasets.Nadir_Reflectance_Band1)/2.0
    )
)

indices.name = "kNDVI"
indices = indices.to_dataset()

indices.to_zarr(f"/net/projects/deep_esdl/data/MODIS/MCD43C4/cubes/modis-mcd43c4-kndvi-no-metadata-256x256x256.zarr")
print(f"NDVI + NIRv + kNDVI took {((datetime.datetime.now() - before).total_seconds())/60} minutes in total")

# print("Computing spectral indices...")

# sigmaPeriod = slice("2000-02-24","2021-12-31")
# sigma = (0.5*(datasets.Nadir_Reflectance_Band2.sel(time=sigmaPeriod) + datasets.Nadir_Reflectance_Band1.sel(time=sigmaPeriod))).median("time")

# indices = spyndex.computeIndex(
#     index = ["NDVI","NIRv","kNDVI"],
#     N = datasets.Nadir_Reflectance_Band2,
#     R = datasets.Nadir_Reflectance_Band1,
#     kNN = 1.0,
#     kNR = spyndex.computeKernel(
#         kernel = "RBF",
#         a = datasets.Nadir_Reflectance_Band2,
#         b = datasets.Nadir_Reflectance_Band1,
#         sigma = sigma
#     )
# )

# indices = indices.to_dataset(dim = "index")

# print("Merging datasets")

# datasets = xr.merge([datasets,indices])

# print("Saving...")
    
# datasets.to_zarr(f"/net/projects/deep_esdl/data/MODIS/MCD43C4/cubes/modis-mcd43c4-vis-no-metadata-256x256x256.zarr")

# print("Done!")
# print(f"Everything took {((datetime.datetime.now() - before).total_seconds())/60} minutes in total")