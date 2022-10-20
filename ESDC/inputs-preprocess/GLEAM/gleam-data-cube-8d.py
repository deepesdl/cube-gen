import xarray as xr
import xesmf as xe
import numpy as np
from tqdm import tqdm
from datetime import datetime

pathOut = "~/data/GLEAM/output"
pathOut = os.path.expanduser(pathOut)

GLEAM = xr.open_zarr(f"{pathOut}/gleam-512x128x128.zarr")

last_year = np.datetime64(GLEAM.time_coverage_end).astype("datetime64[Y]").astype(str).astype(int)
first_year = np.datetime64(GLEAM.time_coverage_start).astype("datetime64[Y]").astype(str).astype(int)

years = np.arange(first_year,last_year + 1)

def resample_weekly(ds,year):
    keep_attrs = ds.time.attrs
    ds = ds.sel(time=slice(f"{year}-01-01",f"{year}-12-31")).resample(time="8D").mean()    
    ds['time'] = ds.time + np.timedelta64(4,"D")
    ds.time.attrs = keep_attrs
    return ds

GLEAM_8d = [resample_weekly(GLEAM,year) for year in tqdm(years)]
GLEAM_8d = xr.concat(GLEAM_8d,dim="time")

GLEAM_8d['crs'] = GLEAM['crs']

GLEAM_8d.attrs['date_modified'] = str(datetime.now())
GLEAM_8d.attrs['time_coverage_end'] = str(GLEAM_8d.time[-1].values)
GLEAM_8d.attrs['time_coverage_start'] = str(GLEAM_8d.time[0].values)
GLEAM_8d.attrs['temporal_resolution'] = "8D"
GLEAM_8d.attrs['time_period'] = "8D"
GLEAM_8d.attrs['reported_day'] = 5.0
GLEAM_8d.attrs['processing_steps'] = GLEAM_8d.attrs['processing_steps'] + ['resampling by 8-day mean']

GLEAM_8d = GLEAM_8d.chunk(dict(time=256,lat=128,lon=128))
GLEAM_8d.attrs['id'] = "256x128x128"

GLEAM_8d.to_zarr(f"{pathOut}/gleam-8d-0.25deg-256x128x128.zarr") # /net/data/GLEAM/gleam-8d-0.25deg-256x128x128.zarr