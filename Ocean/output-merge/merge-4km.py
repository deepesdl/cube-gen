from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os
from datetime import datetime

store_output = new_data_store("s3", root="deep-esdl-output")

pathIn = f"~/data/ocean/source/monthly_global_particulate_organic_carbon_(poc)/"
pathIn = os.path.expanduser(pathIn)

files = glob(f"{pathIn}/*.zarr")
files.sort()

print("Reading files...")
ds = xr.concat([xr.open_zarr(file) for file in tqdm(files)],dim="time")

variables = list(ds.variables)
for dim in ["lat","lon","time"]:
    variables.remove(dim)
    
for variable in variables:
    del ds[variable].encoding['chunks']
    
ds = ds.chunk(dict(time=64,lat=256,lon=256))

additional_attrs = {
    "date_modified": str(datetime.now()),
    "geospatial_lat_max": float(ds.lat.max().values),
    "geospatial_lat_min": float(ds.lat.min().values),
    "geospatial_lat_resolution": abs(float(
        ds.lat[1] - ds.lat[0]
    )),
    "geospatial_lon_max": float(ds.lon.max().values),
    "geospatial_lon_min": float(ds.lon.min().values),
    "geospatial_lon_resolution": abs(float(
        ds.lon[1] - ds.lon[0]
    )),
    "time_coverage_start": str(ds.time[0].values),
    "time_coverage_end": str(ds.time[-1].values),
}

ds.attrs = additional_attrs

print("Writing cube...")
store_output.write_data(ds, "ocean-1M-4km-64x256x256-1.0.0.zarr", replace=True)