from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

from tqdm import tqdm
import xarray as xr
import numpy as np
import os

store = new_data_store("s3", root="deep-esdl-input")
store_output = new_data_store("s3", root="deep-esdl-output")

datasets = [
    'curie_depth_200km_100m.zarr',
    'curie_depth_300km_100m.zarr',
    'geothermal_heat_flow_200km_100m.zarr',
    'geothermal_heat_flow_300km_100m.zarr',
    'geothermal_heat_flow_uncertainty_200km_100m.zarr',
    'geothermal_heat_flow_uncertainty_300km_100m.zarr',
    'ice_thickness_100m.zarr',
    'magnetic_anomaly_100m.zarr',
    'thwaites_sublacial_lakes_2013_2017_100m.zarr'
]

das = [store.open_data(dataset) for dataset in datasets]

def remove_spatial_ref(da):

    if ("spatial_ref" in list(da.coords)) or ("spatial_ref" in list(da.variables)):
        da = da.drop("spatial_ref")
    
    return da

das = [remove_spatial_ref(da) for da in das]
das = xr.merge(das)

rename_dict = dict(
    Thw_124="thw_124",
    Thw_142="thw_142",
    Thw_170="thw_170",
    Thw_70="thw_70",
    mrg="ice_thickness",
)

das = das.rename(rename_dict)

store_output.write_data(
    das, 'polar-100m-1x2048x2048-1.0.0.zarr', replace=True
)