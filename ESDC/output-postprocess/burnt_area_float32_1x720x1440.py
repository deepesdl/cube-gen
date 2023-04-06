from xcube.core.new import new_cube
from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store
from xcube.core.store import new_data_writer

from xcube.core.dsio import open_dataset

data_store = new_data_store("s3", root="deep-esdl-output")

ds = data_store.open_data('esdc-8d-0.25deg-1x720x1440-3.0.1.zarr')

ds['burnt_area'] = ds.burnt_area.astype("float32")

data_store.write_data(ds, 'esdc-8d-0.25deg-1x720x1440-3.0.2.zarr')