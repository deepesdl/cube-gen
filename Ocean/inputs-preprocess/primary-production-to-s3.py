from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os

store_output = new_data_store("s3", root="deep-esdl-input/alicja-test")

pathIn = f"~/data/ocean/source/monthly_global_marine_phytoplankton_primary_production/"
pathIn = os.path.expanduser(pathIn)

files = glob(f"{pathIn}/*.zarr")
files.sort()

print("Reading data...")
ds = xr.concat([xr.open_zarr(file) for file in tqdm(files)],dim="time")

variables = list(ds.variables)
for dim in ["lat","lon","time"]:
    variables.remove(dim)
    
for variable in variables:
    del ds[variable].encoding['chunks']

ds = ds.chunk(dict(time=64,lat=256,lon=256))

print("Writing data...")
store_output.write_data(ds, "phytoplankton-primary-production-1M-9km-64x256x256.zarr", replace=True)