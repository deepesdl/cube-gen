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

store_output = new_data_store("s3", root="deep-esdl-input")

pathIn = f"~/data/hydrology/source/TUWien_RT1_SM/"
pathIn = os.path.expanduser(pathIn)

sites = [(f"0{x}")[-2:] for x in np.arange(1,29)]

def save_site(site):

    files = glob(f"{pathIn}/*{site}/*.zarr")
    files.sort()
    
    ds = xr.concat([xr.open_zarr(file) for file in files],dim="time")
    
    variables = list(ds.variables)
    for dim in ["lat","lon","time"]:
        variables.remove(dim)

    for variable in variables:
        del ds[variable].encoding['chunks']

    ds = ds.chunk(dict(time=128,lat=-1,lon=-1))
    ds = ds.transpose("time","lat","lon")
    
    store_output.write_data(ds, f"hydrology-sm-{site}-128x-1x-1.zarr", replace=True)
    
[save_site(site) for site in tqdm(sites)]