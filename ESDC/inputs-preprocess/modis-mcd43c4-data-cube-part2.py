import xarray as xr
import numpy as np
import spyndex
import glob
import os
import datetime
from tqdm import tqdm

chunks = dict(time=256,lat=256,lon=256)

pathOut = "/net/projects/deep_esdl/data/MODIS/MCD43C4/cubes"

if not os.path.exists(pathOut):
    os.mkdir(pathOut)
    
files = glob.glob("/net/projects/deep_esdl/data/MODIS/MCD43C4/data/*.zarr")
files.sort()

datasets = [xr.open_zarr(file) for file in tqdm(files)]    
datasets = xr.concat(datasets,dim = "time")
datasets = datasets.chunk(chunks)
datasets = datasets.reset_coords().drop("spatial_ref")

# print("Computing spectral indices...")

# indices = spyndex.computeIndex(
#     index = ["NDVI","NIRv","kNDVI","CIG","GNDVI","EVI"],
#     N = datasets.Nadir_Reflectance_Band2,
#     R = datasets.Nadir_Reflectance_Band1,
#     G = datasets.Nadir_Reflectance_Band4,
#     B = datasets.Nadir_Reflectance_Band3,
#     L = spyndex.constants.L.default,
#     g = spyndex.constants.g.default,
#     C1 = spyndex.constants.C1.default,
#     C2 = spyndex.constants.C2.default,
#     kNN = 1.0,
#     kNR = spyndex.computeKernel(
#         kernel = "RBF",
#         a = datasets.Nadir_Reflectance_Band2,
#         b = datasets.Nadir_Reflectance_Band1,
#         sigma = (0.5*(datasets.Nadir_Reflectance_Band2 + datasets.Nadir_Reflectance_Band1)).median("time")
#     )
# )

# indices = indices.to_dataset(dim = "index")

# print("Merging datasets")

# datasets = xr.merge([datasets,indices])

print("Deleting encoding")

variables = [
    'Nadir_Reflectance_Band1',
    'Percent_Inputs',
    'Percent_Snow',
    'BRDF_Albedo_Uncertainty',
    'Nadir_Reflectance_Band2',
    'Nadir_Reflectance_Band3',
    'Nadir_Reflectance_Band4',
    'Nadir_Reflectance_Band5',
    'Nadir_Reflectance_Band6',
    'Nadir_Reflectance_Band7',
    'Albedo_Quality',
    'Local_Solar_Noon'
]

variables = variables # + ["NDVI","NIRv","kNDVI","CIG","GNDVI","EVI"]

for variable in variables:
    del datasets[variable].encoding['chunks']

print("Saving...")
    
datasets.to_zarr(f"{pathOut}/modis-mcd43c4-no-metadata-256x256x256.zarr")

print("Done!")