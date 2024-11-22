import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os
from datetime import datetime, timedelta
import pandas as pd
import sys
from datetime import datetime, timedelta
import pandas as pd
from functools import partial
from dateutil.rrule import rrule, MONTHLY, YEARLY, DAILY


def to_datetime(date):
    """
    Converts a numpy datetime64 object to a python datetime object
    Input:
      date - a np.datetime64 object
    Output:
      DATE - a python datetime object
    """
    timestamp = ((date - np.datetime64('1970-01-01T00:00:00'))
                 / np.timedelta64(1, 's'))
    return datetime.utcfromtimestamp(timestamp)

def check_if_ds_needs_subsetting(ds, start_date, end_date):
    # check if the start and end date should make a subset of the dataset
    time_values = ds.time.values
    time_slice_start = None
    time_slice_end = None
    if start_date > to_datetime(time_values[0]) and start_date < to_datetime(
            time_values[-1]):
        time_slice_start = start_date
    if end_date > to_datetime(time_values[0]) and end_date < to_datetime(
            time_values[-1]):
        time_slice_end = end_date
    if time_slice_start or time_slice_end:
        if not time_slice_start:
            time_slice_start = to_datetime(time_values[0])
        if not time_slice_end:
            time_slice_end = to_datetime(time_values[-1])
        time_slice = slice(time_slice_start, time_slice_end)
        ds = ds.sel(time=time_slice)
    return ds

print ('argument list', sys.argv)
try:
    start_date = sys.argv[1]
except:
    start_date = None

try:
    end_date = sys.argv[2]
except:
    end_date = None

pathIn = f"~/data/hydrology/source/SWE_CPC_GPM_ERA5downT_RadGhent_filter5mm"
pathIn = os.path.expanduser(pathIn)

if start_date:
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        print("You provided a start date, please also provide an end date.")
        exit()
    if end_date < start_date:
        print("The end date must be later than the start date.")
        exit()

    dates = [dt for dt in rrule(YEARLY, dtstart=start_date, until=end_date)]
    files = []
    for date in dates:
        date_files = glob(f"{pathIn}/*{date.year}.nc")
        files.extend(date_files)
    files.sort()

else:
    files = glob(f"{pathIn}/*.nc")
    files.sort()

for file in tqdm(files):
    filename = file.split("/")[-1].replace(".nc",".zarr")
    if not os.path.exists(f"{pathIn}{filename}"):
        ds = xr.open_dataset(file)
        ds = ds.rename(dict(t="time",Y="lat",X="lon"))
        ds["time"] = pd.to_datetime(ds.Time.values-719529, unit='d').values
        ds["lat"] = ds.Lat[:,0]
        ds["lon"] = ds.Lon[0,:]
        ds = ds.drop(["Lon","Lat","Time"])
        if start_date:
            ds = check_if_ds_needs_subsetting(ds, start_date, end_date)
        ds = ds.chunk(dict(time=-1,lon=64,lat=64))
        ds.to_zarr(f"{pathIn}{filename}")