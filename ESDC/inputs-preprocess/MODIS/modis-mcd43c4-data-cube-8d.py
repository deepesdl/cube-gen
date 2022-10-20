import xarray as xr
import xesmf as xe
import numpy as np
from tqdm import tqdm
from datetime import datetime

pathOut = "~/data/MODIS/output"
pathOut = os.path.expanduser(pathOut)

keep_vars = [
    'NDVI',
    'NIRv',
    'Nadir_Reflectance_Band1',
    'Nadir_Reflectance_Band2',
    'Nadir_Reflectance_Band3',
    'Nadir_Reflectance_Band4',
    'Nadir_Reflectance_Band5',
    'Nadir_Reflectance_Band6',
    'Nadir_Reflectance_Band7',
    'crs',
    'kNDVI'
]

dates_2000 = np.arange(np.datetime64("2000-01-05"), np.datetime64("2000-12-31"), np.timedelta64(8, "D")).astype("datetime64[ns]")

dataset = xr.open_zarr(f"{pathOut}/modis-mcd43c4-vis-256x256x256.zarr")

dataset = dataset[keep_vars]

last_year = 2021
first_year = np.datetime64(dataset.time_coverage_start).astype("datetime64[Y]").astype(str).astype(int)

years = np.arange(first_year,last_year + 1)

def resample_weekly(ds,year):
    keep_attrs = ds.time.attrs
    ds = ds.sel(time=slice(f"{year}-01-01",f"{year}-12-31")).resample(time="8D").mean()    
    ds['time'] = ds.time + np.timedelta64(4,"D")
    ds.time.attrs = keep_attrs
    if year==2000:
        ds = ds.interp(coords=dict(time=dates_2000))
    return ds

dataset_8d = [resample_weekly(dataset,year) for year in tqdm(years)]
dataset_8d = xr.concat(dataset_8d,dim="time")

dataset_8d['crs'] = dataset['crs']

dataset_8d.attrs['date_modified'] = str(datetime.now())
dataset_8d.attrs['time_coverage_end'] = str(dataset_8d.time[-1].values)
dataset_8d.attrs['time_coverage_start'] = str(dataset_8d.time[0].values)
dataset_8d.attrs['temporal_resolution'] = "8D"
dataset_8d.attrs['time_period'] = "8D"
dataset_8d.attrs['reported_day'] = 5.0
dataset_8d.attrs['processing_steps'] = dataset_8d.attrs['processing_steps'] + ['resampling by 8-day mean']

dataset_8d = dataset_8d.chunk(dict(time=256,lat=128,lon=128))
dataset_8d.attrs['id'] = "256x128x128"

dataset_8d.to_zarr(f"{pathOut}/modis-mcd43c4-vis-8d-0.05deg-256x128x128.zarr")