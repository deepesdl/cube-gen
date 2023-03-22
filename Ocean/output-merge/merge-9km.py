from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os
from datetime import datetime

store = new_data_store("s3", root="deep-esdl-input")
store_output = new_data_store("s3", root="deep-esdl-output")

datasets = [
    'phytoplankton-primary-production-1M-9km-64x256x256.zarr',
    'oceanic-export-production-1M-9km-64x256x256.zarr',
    'particulate-inorganic-carbon-1M-9km-64x256x256.zarr',
    'particulate-organic-carbon-1M-9km-64x256x256.zarr',
    'phytoplankton-carbon-1M-9km-64x256x256.zarr',
    'dissolved-organic-carbon-1M-9km-64x256x256.zarr'
]

print("Reading files...")

das = [store.open_data(dataset) for dataset in datasets]

for i in [1,2,3,4]:
    das[i]["lat"] = das[0].lat
    das[i]["lon"] = das[0].lon

print("Merging datasets...")
ds = xr.merge(das)

print("Removing unnecessary datasets")
VARIABLES_TO_REMOVE = ["mean_spectral_i_star", "par", "crs"]
ds = ds.drop_vars(VARIABLES_TO_REMOVE)

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
store_output.write_data(ds, "ocean-1M-9km-64x256x256-1.2.0.zarr", replace=True)
