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
    'esacci.AEROSOL.day.L3C.AER_PRODUCTS.AATSR.Envisat.SU.4-3.r1', 
    variable_names=['AOD550_mean'],
    time_range=['2002-05-20','2012-04-08']
)

dates_2002 = np.arange(np.datetime64("2002-05-21"), np.datetime64("2003-01-01"), np.timedelta64(8, "D")).astype("datetime64[ns]")

last_year = 2012
first_year = 2002

years = np.arange(first_year,last_year + 1)

def resample_weekly(ds,year):
    keep_attrs = ds.time.attrs
    ds = ds.sel(time=slice(f"{year}-01-01",f"{year}-12-31")).resample(time="8D").mean()    
    ds['time'] = ds.time + np.timedelta64(4,"D")
    ds.time.attrs = keep_attrs
    if year==2002:
        ds = ds.interp(coords=dict(time=dates_2002))
    return ds

print("Resampling in time")
dataset_8d = [resample_weekly(dataset,year) for year in tqdm(years)]
dataset_8d = xr.concat(dataset_8d,dim="time")

new_lats = np.load("lat.npy")
new_lons = np.load("lon.npy")

print("Resampling in space")
dataset_8d = dataset_8d.interp(coords=dict(lat=new_lats,lon=new_lons),method="nearest")
dataset_8d = dataset_8d.chunk(dict(time=512,lat=128,lon=128))

print("Saving")
dataset_8d.to_zarr("~/data/cci-aod550-8d-0.083deg-512x128x128.zarr")
