from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os

store_output = new_data_store("s3", root="deep-esdl-input")

pathIn = f"~/data/ocean/source/monthly_global_phytoplankton_carbon/"
pathIn = os.path.expanduser(pathIn)

files = glob(f"{pathIn}/*.zarr")
files.sort()

print("Reading data...")
ds = xr.concat([xr.open_zarr(file) for file in tqdm(files)],dim="time")

ds = ds.chunk(dict(time=64))

ds['mean_spectral_i_star'] = ds.mean_spectral_i_star.where(lambda x: x < 9.96921e+36,other = np.nan)

print("Writing data...")
store_output.write_data(ds, "phytoplankton-carbon-1M-9km-64x256x256.zarr", replace=True)