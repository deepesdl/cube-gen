import numpy as np
from tqdm import tqdm
import xarray as xr
import glob

pathIn = "~/data/ERA5/preprocess/yearly"
pathIn = os.path.expanduser(pathIn)

pathOut = "~/data/ERA5/preprocess"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)

files=glob.glob(f"{pathIn}/*.zarr")
files.sort()

print("Reading")
ds=xr.concat([xr.open_zarr(file) for file in tqdm(files)],dim="time")

new_lats = np.arange(-89.875,90,0.25)
new_lons = np.arange(-179.875,180,0.25)

print("Resampling in space")
ds = ds.interp(coords=dict(lat=new_lats,lon=new_lons),method="linear")
ds = ds.chunk(dict(time=256,lat=128,lon=128))

print("Saving")
ds.to_zarr(f"{pathOut}/era5-8d-0.25deg-256x128x128.zarr")