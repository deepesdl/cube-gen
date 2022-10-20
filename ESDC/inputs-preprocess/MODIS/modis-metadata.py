from tqdm import tqdm
from datetime import datetime
import yaml
import rioxarray
import xarray as xr
import numpy as np

pathSource = "~/data/MODIS/source"
patpathSourcehIn = os.path.expanduser(pathSource)

pathIn = "~/data/MODIS/preprocess"
pathIn = os.path.expanduser(pathIn)

pathOut = "~/data/MODIS/output"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)

with open("modis-metadata.yaml", "r") as stream:
    try:
        metadata = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

datacube = xr.open_zarr(f"{pathIn}/modis-mcd43c4-vis-256x256x256.zarr")

ref = xr.open_zarr(f"{pathSource}/MCD43C4.A2000055.061.2020038224934.zarr")

datacube = datacube.rio.write_crs(
    ref.rio.crs, grid_mapping_name="crs"
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

datacube.to_zarr(f"{pathOut}/modis-mcd43c4-vis-256x256x256.zarr")
