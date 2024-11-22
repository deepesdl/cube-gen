import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os
from datetime import datetime, timedelta
import pandas as pd
from functools import partial
import sys

print ('argument list', sys.argv)
try:
    start_date = sys.argv[1]
except:
    start_date = None

try:
    end_date = sys.argv[2]
except:
    end_date = None



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

pathIn = f"~/data/hydrology/source/precipitation_GPM_CPC_SM2RAIN-ASCAT/"
pathIn = os.path.expanduser(pathIn)

files = glob(f"{pathIn}/*.nc")
files.sort()

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

for file in tqdm(files):
    filename = file.split("/")[-1].replace(".nc",".zarr")
    if not os.path.exists(f"{pathIn}{filename}"):
        ds = xr.open_dataset(file)
        if start_date:
            ds = check_if_ds_needs_subsetting(ds, start_date, end_date)
        ds = ds.chunk(dict(time=128,lon=-1,lat=-1))
        ds.to_zarr(f"{pathIn}{filename}")