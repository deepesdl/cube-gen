from geojson import Feature, Polygon, dump
import shapely

import xarray as xr
import numpy as np

from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

store_output = new_data_store("s3", root="deep-esdl-output")
bs = store_output.open_data("esdc-8d-0.25deg-256x128x128-3.0.0.zarr")

cube_json = bs.to_dict(data=False)

variables = []
for key, value in cube_json["data_vars"].items():
    if key != "crs":
        variables.append({"name": key, **value["attrs"]})

BBox_coords = [
    cube_json["attrs"]["geospatial_lon_min"],
    cube_json["attrs"]["geospatial_lat_min"],
    cube_json["attrs"]["geospatial_lon_max"],
    cube_json["attrs"]["geospatial_lat_max"],
]

BBox = shapely.geometry.box(
    BBox_coords[0], BBox_coords[1], BBox_coords[2], BBox_coords[3]
)

polygon = [[[x[0], x[1]] for x in list(BBox.exterior.coords)]]

with open("esdc.geojson", "w") as f:
    dump(
        Feature(
            geometry=Polygon(polygon),
            properties={**cube_json["attrs"], "variables": variables},
        ),
        f,
        indent=4,
    )