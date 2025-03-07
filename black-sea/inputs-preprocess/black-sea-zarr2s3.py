from tqdm import tqdm
from datetime import datetime
import yaml
import xarray as xr
import numpy as np

from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

with tqdm(total=80) as pbar:

    FINAL_CHUNKS = dict(time=256, lat=256, lon=256)

    store = new_data_store("s3", root="deep-esdl-input")

    def sort_and_cast_by_time(ds):
        ds = ds.sortby(ds.time)
        ds["time"] = ds.time.astype("datetime64[D]")
        return ds

    pbar.update(10)
    pbar.set_description("Processing reference dataset (Chl)")

    chl = store.open_data("EO4SIBS-black-sea-chl.zarr")
    chl = sort_and_cast_by_time(chl)
    chl = chl * 0.01
    chl_spatial = dict(lat=chl.lat, lon=chl.lon)
    chl = chl.chunk(FINAL_CHUNKS)
    
    pbar.update(10)
    pbar.set_description("Processing additional dataset (wave height)")
    
    bswh = store.open_data("CMEMS-black-sea-wave-height.zarr")
    bswh_time_aggregated = bswh.sortby(bswh.time).resample(time="1D").mean()
    bswh_time_aggregated = bswh_time_aggregated.sel(
        time=slice("2016-01-01", "2017-12-31")
    )
    bswh_spatial_resampled = bswh_time_aggregated.interp(
        coords=chl_spatial, method="nearest"
    )
    bswh_time_aggregated = bswh_time_aggregated.chunk(FINAL_CHUNKS)
    
    pbar.update(10)
    pbar.set_description("Processing additional dataset (altimetry)")

    bsa = store.open_data("EO4SIBS-black-sea-altimetry.zarr")
    bsa_time_sorted = sort_and_cast_by_time(bsa)
    bsa_spatial_resampled = bsa_time_sorted.interp(coords=chl_spatial, method="nearest")
    bsa_spatial_resampled = bsa_spatial_resampled.chunk(FINAL_CHUNKS)
    
    pbar.update(10)
    pbar.set_description("Processing additional dataset (SSS)")

    sss = store.open_data("EO4SIBS-black-sea-sss.zarr")
    sss_time_sorted = sort_and_cast_by_time(sss).drop_duplicates(dim="time")
    sss_spatial_resampled = sss_time_sorted.interp(coords=chl_spatial, method="nearest")
    sss_spatial_resampled = sss_spatial_resampled.chunk(FINAL_CHUNKS)

    pbar.update(10)
    pbar.set_description("Processing additional dataset (SST)")

    sst = store.open_data("CMEMS-black-sea-sst.zarr")
    sst_time_sorted = sort_and_cast_by_time(sst)
    sst_spatial_resampled = sst_time_sorted.interp(coords=chl_spatial, method="nearest")
    sst_spatial_resampled = sst_spatial_resampled.chunk(FINAL_CHUNKS)

    pbar.update(20)
    pbar.set_description("Writing dataset's")

    store.write_data(
        chl, "EO4SIBS-black-sea-chl-256x256x256.zarr", replace=True
    )

    store.write_data(
        bswh_time_aggregated, "CMEMS-black-sea-wave-height-256x256x256.zarr", replace=True
    )

    store.write_data(
        bsa_spatial_resampled, "EO4SIBS-black-sea-altimetry-256x256x256.zarr", replace=True
    )

    store.write_data(
        sss_spatial_resampled, "EO4SIBS-black-sea-sss-256x256x256.zarr", replace=True
    )

    store.write_data(
        sst_spatial_resampled, "CMEMS-black-sea-sst-256x256x256.zarr", replace=True
    )

    pbar.update(10)
    pbar.set_description("Done")
    