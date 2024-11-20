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

sites = [(f"0{x}")[-2:] for x in np.arange(1,29)]

def chunk_and_create_encoding_dict(ds,
                                   time_chunking,
                                   lat_chunking,
                                   lon_chunking,
                                   quiet=True):
    
    for var_name in ds.data_vars:
        if var_name != "crs":
            if not quiet:
                print(var_name)
            ds[var_name] = ds[var_name].chunk({'time': time_chunking,
                                               'lat': lat_chunking,
                                               'lon': lon_chunking})
            
    encoding_dict = dict()
    
    coords_encoding = {k: dict(chunks=v.shape) for k, v in ds.coords.items()}
    vars_encoding = {k: dict(chunks=(time_chunking,
                                     lat_chunking,
                                     lon_chunking),
                             dtype=np.dtype('float32'),
                             write_empty_chunks=False) for k, v in ds.data_vars.items() if k != "crs"}
    
    encoding_dict.update(coords_encoding)
    encoding_dict.update(vars_encoding)
    
    return ds, encoding_dict

def save_site(site):
    
    datasets = [
        f'hydrology-evaporation-{site}-64x-1x-1.zarr',
        f'hydrology-precipitation-{site}-64x-1x-1.zarr',
        f'hydrology-swe-{site}-64x-1x-1.zarr',
        f'hydrology-sm-{site}-128x-1x-1.zarr'
    ]
    
    das = [store.open_data(dataset) for dataset in datasets]
    
    ref_lat = das[0].lat
    ref_lon = das[0].lon
    
    for i in range(len(das)):
        das[i]["lat"] = ref_lat
        das[i]["lon"] = ref_lon
        
    ds = xr.merge(das)
    
    variables = list(ds.variables)
    for dim in ["lat","lon","time"]:
        variables.remove(dim)

    for variable in variables:
        del ds[variable].encoding['chunks']

    lat_chunking = ds.lat.shape[0]
    lon_chunking = ds.lon.shape[0]
    time_chunking = 1

    ds = ds.resample(time='1D').mean(skipna=True, keep_attrs=True)
    ds, encoding_dict = chunk_and_create_encoding_dict(ds,
                                                       time_chunking,
                                                       lat_chunking,
                                                       lon_chunking,
                                                       True)

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
    
    store_output.write_data(
        ds,
        f"hydrology-S{site}-0.009deg-1D-{time_chunking}x{lat_chunking}x{lon_chunking}-1.0.0.zarr",
        replace=True,
        encoding=encoding_dict
    )
    
[save_site(site) for site in tqdm(sites)]