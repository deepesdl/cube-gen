from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os
from datetime import datetime, timedelta
import pandas as pd

store_output = new_data_store("s3", root="deep-esdl-input/alicja_test_2")

pathIn = f"~/data/hydrology/source/SWE_CPC_GPM_ERA5downT_RadGhent_filter5mm/"
pathIn = os.path.expanduser(pathIn)

sites = [(f"0{x}")[-2:] for x in np.arange(1,29)]

def save_site(site):

    files = glob(f"{pathIn}/*d{site}*.zarr")
    files.sort()
    
    ds = xr.concat([xr.open_zarr(file) for file in files],dim="time")
    ds = ds.sortby("lat",ascending=False)
    
    variables = list(ds.variables)
    for dim in ["lat","lon","time"]:
        variables.remove(dim)

    for variable in variables:
        del ds[variable].encoding['chunks']

    ds = ds.chunk(dict(time=64,lat=-1,lon=-1))
    
    store_output.write_data(ds, f"hydrology-swe-{site}-64x-1x-1.zarr", replace=True)
    
[save_site(site) for site in tqdm(sites)]