from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

from tqdm import tqdm
import xarray as xr
import numpy as np
import os
from glob import glob

store_output = new_data_store("s3", root="deep-esdl-input/alicja-testing")

cubes = glob(os.path.expanduser("~/data/polar/cubes/*"))
cubes.sort()
cubes = [glob(f"{cube}/*100m.zarr")[0] for cube in cubes]

def upload_cube(cube):
    filename = cube.split("/")[-1]
    da = xr.open_zarr(cube)
    store_output.write_data(da, filename, replace=True)
    
[upload_cube(cube) for cube in tqdm(cubes)]