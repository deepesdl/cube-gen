import os

import numpy as np
from xcube.core.store import new_data_store

pathOut = "~/data/CCI/cloud/preprocess"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)

print("Reading")
store = new_data_store('cciodp')

dataset = store.open_data(
    'esacci.CLOUD.mon.L3C.CLD_PRODUCTS.MODIS.Terra.MODIS_TERRA.2-0.r1',
    variable_names=['cot', 'cth', 'ctt'],
    time_range=["2000-02-01", "2014-12-31"]
)

dataset = dataset.drop([x for x in list(dataset.variables) if
                        x not in ['time', 'lat', 'lon', 'cot', 'cth', 'ctt']])

dataset = dataset.chunk(dict(time=-1, lat=64, lon=64))


def get_dates_8d(year):
    return np.arange(np.datetime64(f"{year}-01-05"),
                     np.datetime64(f"{year + 1}-01-01"),
                     np.timedelta64(8, "D")).astype("datetime64[ns]")


dates = np.concatenate([get_dates_8d(year) for year in np.arange(2000, 2015)])
dates = dates[(dates >= np.datetime64("2000-02-15")) & (
            dates <= np.datetime64("2014-12-16"))]

print("Resampling in time")
dataset_8d = dataset.interp(coords=dict(time=dates), method="nearest")

new_lats = np.load("lat.npy")
new_lons = np.load("lon.npy")

print("Resampling in space")
dataset_8d = dataset_8d.interp(coords=dict(lat=new_lats, lon=new_lons),
                               method="nearest")
dataset_8d = dataset_8d.chunk(dict(time=256, lat=128, lon=128))

print("Saving")
dataset_8d.to_zarr(f"{pathOut}/cci-cloud-8d-0.083deg-256x128x128.zarr")
