import xarray as xr
import numpy as np
import glob
import os

from tqdm import tqdm

# pathOut = "/Net/Groups/BGI/work_1/scratch/dmontero/ERA5/yearly"

# if not os.path.exists(pathOut):
#     os.mkdir(pathOut)

pathIn = "~/data/ERA5/preprocess/monthly"
pathIn = os.path.expanduser(pathIn)

pathOut = "~/data/ERA5/preprocess/yearly"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)

def resample_8d(year):
    files=glob.glob(f"{pathIn}/*{year}*.zarr")
    files.sort()
    ds=xr.concat([xr.open_zarr(file) for file in files],dim="time")
    ds_mean=ds[['e','ssr','t2m','tp']].resample(time="8D").mean()
    ds_max=ds[['t2m_max']].resample(time="8D").max()
    ds_min=ds[['t2m_min']].resample(time="8D").min()
    ds=xr.merge([ds_mean,ds_max,ds_min])
    ds=ds.chunk(dict(time=-1))
    ds.to_zarr(f"{pathOut}/era5-{year}.zarr")
    
[resample_8d(year) for year in np.arange(1979,2022)]