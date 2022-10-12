from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

import shapely.geometry
from IPython.display import JSON
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import xarray as xr

print("Reading")
store = new_data_store('cciodp')

dataset = store.open_data(
    'esacci.CLOUD.mon.L3C.CLD_PRODUCTS.MODIS.Terra.MODIS_TERRA.2-0.r1', 
    variable_names=['cot','cth','ctt'],
    time_range=["2000-02-01","2014-12-31"]
)

dataset = dataset.drop([x for x in list(dataset.variables) if x not in ['time','lat','lon','cot','cth','ctt']])

dataset = dataset.chunk(dict(time=-1,lat=64,lon=64))

def get_dates_8d(year):
    return np.arange(np.datetime64(f"{year}-01-05"), np.datetime64(f"{year+1}-01-01"), np.timedelta64(8, "D")).astype("datetime64[ns]")

dates = np.concatenate([get_dates_8d(year) for year in np.arange(2000,2015)])
dates = dates[(dates >= np.datetime64("2000-02-15")) & (dates <= np.datetime64("2014-12-16"))]

print("Resampling in time")
dataset_8d = dataset.interp(coords=dict(time=dates),method="nearest")

new_lats = np.arange(-89.875,90,0.25)
new_lons = np.arange(-179.875,180,0.25)

print("Resampling in space")
dataset_8d = dataset_8d.interp(coords=dict(lat=new_lats,lon=new_lons),method="nearest")
dataset_8d = dataset_8d.chunk(dict(time=256,lat=128,lon=128))

print("Saving")
dataset_8d.to_zarr("~/data/cci-cloud-8d-0.25deg-256x128x128.zarr")