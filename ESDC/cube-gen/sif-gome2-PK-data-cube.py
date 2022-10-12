import xarray as xr
import numpy as np
import glob
import os
import datetime
from tqdm import tqdm

pathOut = "/net/projects/deep_esdl/data/GOME2-SIF/cubes/"

if not os.path.exists(pathOut):
    os.mkdir(pathOut)
    
files = glob.glob(f"/net/projects/deep_esdl/data/GOME2-SIF/data/*PK*.nc")
files.sort()

datasets = [xr.open_dataset(file,chunks = {'lat':256, 'lon':256, 'time':256}) for file in files]
datasets = xr.concat(datasets,dim = "time").drop("crs")
datasets = datasets.transpose("time","lat","lon")
datasets = datasets.chunk({'lat':256, 'lon':256, 'time':256})

datasets.to_zarr(f"{pathOut}/sif-gome2-PK-256x256x256.zarr")
