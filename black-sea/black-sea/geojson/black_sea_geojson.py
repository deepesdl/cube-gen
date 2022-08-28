from geojson import Feature, Polygon, dump
import shapely

import xarray as xr
import numpy as np

from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

store_output = new_data_store("s3", root="deep-esdl-output")
bs = store_output.open_data("black-sea-256x128x128.zarr")

cube_json = bs.to_dict(data=False)

additional_properties = {
    "chl": {
        "original_lon_spatial_res": 0.003,
        "original_lat_spatial_res": 0.003,
        "original_name": "Chlorophyll",
        "original_scale_factor": 0.01,
        "original_add_offset": 0.0,
        "original_time_period": "1D",
        "processing_steps": ["Multiplying original scale factor"],
    },
    "sla": {
        "original_lon_spatial_res": 0.0625,
        "original_lat_spatial_res": 0.0625,
        "original_name": "sla",
        "original_scale_factor": 1.0,
        "original_add_offset": 0.0,
        "original_time_period": "1D",
        "processing_steps": ["Spatial nearest neighbor interpolation"],
    },
    "ugos": {
        "original_lon_spatial_res": 0.0625,
        "original_lat_spatial_res": 0.0625,
        "original_name": "ugos",
        "original_scale_factor": 1.0,
        "original_add_offset": 0.0,
        "original_time_period": "1D",
        "processing_steps": ["Spatial nearest neighbor interpolation"],
    },
    "ugosa": {
        "original_lon_spatial_res": 0.0625,
        "original_lat_spatial_res": 0.0625,
        "original_name": "ugosa",
        "original_scale_factor": 1.0,
        "original_add_offset": 0.0,
        "original_time_period": "1D",
        "processing_steps": ["Spatial nearest neighbor interpolation"],
    },
    "vgos": {
        "original_lon_spatial_res": 0.0625,
        "original_lat_spatial_res": 0.0625,
        "original_name": "vgos",
        "original_scale_factor": 1.0,
        "original_add_offset": 0.0,
        "original_time_period": "1D",
        "processing_steps": ["Spatial nearest neighbor interpolation"],
    },
    "vgosa": {
        "original_lon_spatial_res": 0.0625,
        "original_lat_spatial_res": 0.0625,
        "original_name": "vgosa",
        "original_scale_factor": 1.0,
        "original_add_offset": 0.0,
        "original_time_period": "1D",
        "processing_steps": ["Spatial nearest neighbor interpolation"],
    },
    "sss": {
        "original_lon_spatial_res": 0.25,
        "original_lat_spatial_res": 0.25,
        "original_name": "sss",
        "original_scale_factor": 1.0,
        "original_add_offset": 0.0,
        "original_time_period": "1D",
        "processing_steps": ["Spatial nearest neighbor interpolation"],
    },
    "VHM0": {
        "original_lon_spatial_res": 0.037,
        "original_lat_spatial_res": 0.028,
        "original_name": "VHM0",
        "original_scale_factor": 1.0,
        "original_add_offset": 0.0,
        "original_time_period": "1H",
        "processing_steps": [
            "Temporal daily mean aggregation",
            "Spatial nearest neighbor interpolation",
        ],
    },
    "sst": {
        "original_lon_spatial_res": 0.00833,
        "original_lat_spatial_res": 0.00833,
        "original_name": "sea_surface_temperature",
        "original_scale_factor": 1.0,
        "original_add_offset": 0.0,
        "original_time_period": "1D",
        "processing_steps": ["Spatial nearest neighbor interpolation"],
    },
}

variables = []
for key, value in cube_json["data_vars"].items():
    if key != "crs":
        variables.append({"name": key, **value["attrs"], **additional_properties[key]})

BBox_coords = [
    cube_json["attrs"]["geospatial_lon_min"],
    cube_json["attrs"]["geospatial_lat_min"],
    cube_json["attrs"]["geospatial_lon_max"],
    cube_json["attrs"]["geospatial_lat_max"],
]

BBox = shapely.geometry.box(
    BBox_coords[0],
    BBox_coords[1],
    BBox_coords[2],
    BBox_coords[3],
)

polygon = [[[x[0], x[1]] for x in list(BBox.exterior.coords)]]

with open("black-sea.geojson", "w") as f:
    dump(
        Feature(
            geometry=Polygon(polygon),
            properties={**cube_json["attrs"], "variables": variables},
        ),
        f,
    )
