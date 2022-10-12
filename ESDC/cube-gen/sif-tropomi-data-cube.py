import xarray as xr
import numpy as np
import glob
import os

pathOut = "/net/projects/deep_esdl/data/TROPOMI/cubes/"

if not os.path.exists(pathOut):
    os.mkdir(pathOut)
    
files = glob.glob("/net/projects/deep_esdl/data/TROPOMI/data/*8-daily.nc")
files.sort()

datasets = [xr.open_dataset(file,chunks = {'lat':256, 'lon':256, 'time':256}) for file in files]
datasets = xr.concat(datasets,dim = "time")
datasets = datasets.transpose("time","lat","lon")
datasets = datasets.chunk({'lat':128, 'lon':128, 'time':256})

datasets.to_zarr(f"{pathOut}/sif-tropomi-no-metadata-176x128x128.zarr")
