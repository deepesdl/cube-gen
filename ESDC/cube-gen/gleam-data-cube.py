import xarray as xr
import numpy as np
import glob
import os
import datetime
from tqdm import tqdm

pathOut = "/net/projects/deep_esdl/data/GLEAM/cubes/"

if not os.path.exists(pathOut):
    os.mkdir(pathOut)

years = np.arange(1980,2022)

yearly_datasets = []

for year in tqdm(years):

    files = glob.glob(f"/net/projects/deep_esdl/data/GLEAM/data/v3.6a/daily/{year}/*.nc")
    files.sort()

    datasets = [xr.open_dataset(file,chunks = {'time':512,'lat':128,'lon':128}) for file in files]

    yearly_dataset = xr.merge(datasets)
    
    yearly_datasets.append(yearly_dataset)
    
full_dataset = xr.concat(yearly_datasets,dim = "time")
full_dataset = full_dataset.transpose("time","lat","lon")
full_dataset = full_dataset.chunk({'time':512,'lat':128,'lon':128})

full_dataset.to_zarr(f"{pathOut}/gleam-no-metadata-512x128x128.zarr")
