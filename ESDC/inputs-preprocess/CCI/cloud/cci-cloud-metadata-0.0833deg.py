import os
from datetime import datetime

import xarray as xr
import yaml

pathIn = "~/data/CCI/cloud/preprocess"
pathIn = os.path.expanduser(pathIn)

pathOut = "~/data/CCI/cloud/output"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)

with open("inputs-preprocess/CCI/cloud/cci-cloud-metadata-0.0833deg.yaml",
          "r") as stream:
    try:
        metadata = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

datacube = xr.open_zarr(f"{pathIn}/cci-cloud-8d-0.083deg-256x128x128.zarr")

datacube = datacube.rio.write_crs(
    "epsg:4326", grid_mapping_name="crs"
).reset_coords()
del datacube.crs.attrs["spatial_ref"]

datacube.attrs = metadata["global"]

for variable, attributes in metadata["local"].items():
    datacube[variable].attrs = dict(sorted(attributes.items()))

additional_attrs = {
    "date_modified": str(datetime.now()),
    "geospatial_lat_max": float(datacube.lat.max().values),
    "geospatial_lat_min": float(datacube.lat.min().values),
    "geospatial_lat_resolution": float(
        datacube.lat[1] - datacube.lat[0]
    ),
    "geospatial_lon_max": float(datacube.lon.max().values),
    "geospatial_lon_min": float(datacube.lon.min().values),
    "geospatial_lon_resolution": float(
        datacube.lon[1] - datacube.lon[0]
    ),
    "time_coverage_start": str(datacube.time[0].values),
    "time_coverage_end": str(datacube.time[-1].values),
}

datacube.attrs = dict(
    sorted({**datacube.attrs, **additional_attrs}.items())
)

datacube.to_zarr(f"{pathOut}/cci-cloud-8d-0.083deg-256x128x128.zarr")
