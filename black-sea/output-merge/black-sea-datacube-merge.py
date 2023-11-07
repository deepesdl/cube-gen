from tqdm import tqdm
from datetime import datetime
import yaml
import rioxarray
import xarray as xr
import numpy as np

from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store


with tqdm(total=80) as pbar:
    
    with open("../output-postprocess/black-sea-metadata.yaml", "r") as stream:
        try:
            metadata = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    store = new_data_store("s3", root="deep-esdl-input")
    store_output = new_data_store("s3", root="deep-esdl-output")
    
    pbar.update(10)
    pbar.set_description("Loading datasets")
    
    chl = store.open_data("EO4SIBS-black-sea-chl-256x256x256.zarr")
    bswh =  store.open_data("CMEMS-black-sea-wave-height-256x256x256.zarr")
    bsa =  store.open_data("EO4SIBS-black-sea-altimetry-256x256x256.zarr")
    sss =  store.open_data("EO4SIBS-black-sea-sss-256x256x256.zarr")
    sst =  store.open_data("CMEMS-black-sea-sst-256x256x256.zarr")
    
    pbar.update(10)
    pbar.set_description("Merging datasets")
    
    black_sea_datacube = xr.merge(
        [
            chl,
            bswh,
            bsa,
            sss,
            sst,
        ]
    )
    
    pbar.update(10)
    pbar.set_description("Adding attributes")

    black_sea_datacube = black_sea_datacube.rio.write_crs(
        "epsg:4326", grid_mapping_name="crs"
    ).reset_coords()
    del black_sea_datacube.crs.attrs["spatial_ref"]

    black_sea_datacube.attrs = metadata["global"]

    for variable, attributes in metadata["local"].items():
        black_sea_datacube[variable].attrs = dict(sorted(attributes.items()))

    additional_attrs = {
        "date_modified": str(datetime.now()),
        "geospatial_lat_max": float(black_sea_datacube.lat.max().values),
        "geospatial_lat_min": float(black_sea_datacube.lat.min().values),
        "geospatial_lat_resolution": float(
            black_sea_datacube.lat[1] - black_sea_datacube.lat[0]
        ),
        "geospatial_lon_max": float(black_sea_datacube.lon.max().values),
        "geospatial_lon_min": float(black_sea_datacube.lon.min().values),
        "geospatial_lon_resolution": float(
            black_sea_datacube.lon[1] - black_sea_datacube.lon[0]
        ),
        "time_coverage_start": str(black_sea_datacube.time[0].values),
        "time_coverage_end": str(black_sea_datacube.time[-1].values),
    }

    black_sea_datacube.attrs = dict(
        sorted({**black_sea_datacube.attrs, **additional_attrs}.items())
    )

    pbar.update(20)
    pbar.set_description("Writing dataset")

    store_output.write_data(
        black_sea_datacube, f'{black_sea_datacube.attrs["id"]}.zarr', replace=True
    )

    pbar.update(10)
    pbar.set_description("Done")