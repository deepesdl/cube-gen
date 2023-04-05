from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os

store_output = new_data_store("s3", root="deep-esdl-input")

pathIn = f"~/data/ocean/source/particulate_inorganic_carbon/"
pathIn = os.path.expanduser(pathIn)

files = glob(f"{pathIn}/*.zarr")
files.sort()

ref_da = xr.open_zarr(files[0])
ref_lat = ref_da.lat
ref_lon = ref_da.lon

def open_zarr_with_coords_like(file):
    da = xr.open_zarr(file)
    da["lat"] = ref_lat
    da["lon"] = ref_lon
    return da    

print("Reading data...")
ds = xr.concat([open_zarr_with_coords_like(file) for file in tqdm(files)],dim="time")

print("Sorting by latitude..")
ds = ds.sortby("lat")

variables = list(ds.variables)
for dim in ["lat","lon","time"]:
    variables.remove(dim)

for variable in variables:
    del ds[variable].encoding['chunks']

ds = ds.chunk(dict(time=64,lat=256,lon=256))

print("Writing data...")
store_output.write_data(ds, "particulate-inorganic-carbon-1M-9km-64x256x256.zarr", replace=True)
