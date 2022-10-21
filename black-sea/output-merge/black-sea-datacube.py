from tqdm import tqdm
from datetime import datetime
import yaml
import rioxarray
import xarray as xr
import numpy as np

from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

with tqdm(total=100) as pbar:

    pbar.set_description("Reading metadata and opening stores")

    with open("../output-postprocess/black-sea-metadata.yaml", "r") as stream:
        try:
            metadata = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    FINAL_CHUNKS = dict(time=256, lat=256, lon=256)

    store = new_data_store("s3", root="deep-esdl-input")
    store_output = new_data_store("s3", root="deep-esdl-output")

    def sort_and_cast_by_time(ds):
        ds = ds.sortby(ds.time)
        ds["time"] = ds.time.astype("datetime64[D]")
        return ds

    pbar.update(10)
    pbar.set_description("Processing reference dataset (Chl)")

    ref = store.open_data("EO4SIBS-black-sea-chl.zarr")
    ref = sort_and_cast_by_time(ref)
    ref = ref * 0.01
    ref_spatial = dict(lat=ref.lat, lon=ref.lon)

    pbar.update(10)
    pbar.set_description("Processing additional dataset (wave height)")

    bswh = store.open_data("CMEMS-black-sea-wave-height.zarr")
    bswh_time_aggregated = bswh.sortby(bswh.time).resample(time="1D").mean()
    bswh_time_aggregated = bswh_time_aggregated.sel(
        time=slice("2016-01-01", "2017-12-31")
    )
    bswh_spatial_resampled = bswh_time_aggregated.interp(
        coords=ref_spatial, method="nearest"
    )

    pbar.update(10)
    pbar.set_description("Processing additional dataset (altimetry)")

    bsa = store.open_data("EO4SIBS-black-sea-altimetry.zarr")
    bsa_time_sorted = sort_and_cast_by_time(bsa)
    bsa_spatial_resampled = bsa_time_sorted.interp(coords=ref_spatial, method="nearest")

    pbar.update(10)
    pbar.set_description("Processing additional dataset (SSS)")

    sss = store.open_data("EO4SIBS-black-sea-sss.zarr")
    sss_time_sorted = sort_and_cast_by_time(sss).drop_duplicates(dim="time")
    sss_spatial_resampled = sss_time_sorted.interp(coords=ref_spatial, method="nearest")

    pbar.update(10)
    pbar.set_description("Processing additional dataset (SST)")

    sst = store.open_data("CMEMS-black-sea-sst.zarr")
    sst_time_sorted = sort_and_cast_by_time(sst)
    sst_spatial_resampled = sst_time_sorted.interp(coords=ref_spatial, method="nearest")

    pbar.update(10)
    pbar.set_description("Merging datasets")

    black_sea_datacube = xr.merge(
        [
            ref,
            bswh_spatial_resampled,
            bsa_spatial_resampled,
            sss_spatial_resampled,
            sst_spatial_resampled,
        ]
    )

    black_sea_datacube = black_sea_datacube.chunk(FINAL_CHUNKS)

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
