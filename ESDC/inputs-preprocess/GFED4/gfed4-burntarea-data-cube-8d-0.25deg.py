import xarray as xr
import rioxarray
import numpy as np
import glob
import os
import datetime
from tqdm import tqdm

pathIn = "path-to-GFED4-folder"

pathOut = "~/data/GFED4/preprocess"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)

files = glob.glob(f"{pathIn}/*.hdf")
files.sort()

print("Reading")
def read_and_chunk(file):

    filename = file.split("/")[-1]
    date = filename.split("_")[2]
    date = np.datetime64(datetime.datetime.strptime(date, '%Y%m')) + np.timedelta64(15,"D")
    
    ds = rioxarray.open_rasterio(file)
    ds = (ds[['0']].sel(band=1) * 0.01).drop(["band","spatial_ref"])

    ds['x'] = np.arange(-179.875,180,0.25)
    ds['y'] = np.arange(89.875,-90,-0.25)

    ds = ds.rename({"y": "lat", "x":"lon","0": "burnt_area"})
    ds = ds.assign_coords({"time": date}).expand_dims("time")
    ds = ds.transpose("time","lat","lon")
    ds = ds.chunk(dict(time=1,lat=128,lon=128))
    
    return ds

dataset = xr.concat([read_and_chunk(file) for file in tqdm(files)],dim="time")

dataset = dataset.chunk(dict(time=-1))

def get_dates_8d(year):
    return np.arange(np.datetime64(f"{year}-01-05"), np.datetime64(f"{year+1}-01-01"), np.timedelta64(8, "D")).astype("datetime64[ns]")

dates = np.concatenate([get_dates_8d(year) for year in np.arange(1995,2017)])
dates = dates[(dates >= np.datetime64("1995-06-01")) & (dates <= np.datetime64("2016-12-31"))]

print("Resampling in time")
dataset_8d = dataset.interp(coords=dict(time=dates),method="nearest",kwargs={"fill_value": "extrapolate"})

dataset_8d.chunk(dict(time=256))

print("Saving")
dataset_8d.to_zarr(f"{pathOut}/gfed4-burntarea-8d-0.25deg-256x128x128.zarr")