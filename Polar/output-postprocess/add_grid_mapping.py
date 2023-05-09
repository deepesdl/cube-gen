from xcube.core.store import new_data_store

import xarray as xr
import rioxarray

store_output = new_data_store("s3", root="deep-esdl-output")

ds = store_output.open_data('polar-100m-1x2048x2048-1.0.0.zarr')

ds = ds.rio.write_crs("epsg:3031",grid_mapping_name="crs").reset_coords()

store_output.write_data(
    ds, 'polar-100m-1x2048x2048-1.0.1.zarr', replace=True
)