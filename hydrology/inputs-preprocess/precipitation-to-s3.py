from xcube.core.store import new_data_store

import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os


store_output = new_data_store("s3", root="deep-esdl-input")

pathIn = f"~/data/hydrology/source/precipitation_GPM_CPC_SM2RAIN-ASCAT/"
pathIn = os.path.expanduser(pathIn)

sites = [(f"0{x}")[-2:] for x in np.arange(1,29)]

def save_site(site):

    file = glob(f"{pathIn}/*_{site}precip*.zarr")[0]
    
    ds = xr.open_zarr(file)
    
    variables = list(ds.variables)
    for dim in ["lat","lon","time"]:
        variables.remove(dim)

    for variable in variables:
        del ds[variable].encoding['chunks']

    ds = ds.chunk(dict(time=64,lat=-1,lon=-1))
      
    store_output.write_data(ds, f"hydrology-precipitation-{site}-64x-1x-1.zarr", replace=True)
    
[save_site(site) for site in tqdm(sites)]