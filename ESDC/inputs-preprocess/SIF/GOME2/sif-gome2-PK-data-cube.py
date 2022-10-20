import xarray as xr
import numpy as np
import glob
import os
import datetime
from tqdm import tqdm

# pathOut = "/net/projects/deep_esdl/data/GOME2-SIF/cubes/"

# if not os.path.exists(pathOut):
#    os.mkdir(pathOut)

pathIn = "~/data/SIF/GOME2-SIF/source"
pathIn = os.path.expanduser(pathIn)

pathOut = "~/data/SIF/GOME2-SIF/preprocess"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)
    
files = glob.glob(f"{pathIn}/*PK*.nc")
files.sort()

datasets = [xr.open_dataset(file,chunks = {'lat':256, 'lon':256, 'time':256}) for file in files]
datasets = xr.concat(datasets,dim = "time").drop("crs")
datasets = datasets.transpose("time","lat","lon")
datasets = datasets.chunk({'lat':256, 'lon':256, 'time':256})

datasets.to_zarr(f"{pathOut}/sif-gome2-PK-256x256x256.zarr")
