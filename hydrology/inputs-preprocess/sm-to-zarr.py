import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os
import sys
from datetime import datetime, timedelta
import pandas as pd
from functools import partial
from dateutil.rrule import rrule, DAILY

try:
    start_date = sys.argv[1]
except:
    start_date = None

try:
    end_date = sys.argv[2]
except:
    end_date = None

pathIn = f"~/data/hydrology/source/TUWien_RT1_SM"
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

    dates = [dt for dt in rrule(DAILY, dtstart=start_date, until=end_date)]
    files = []
    for date in dates:
        date_files = glob(f"{pathIn}/*/{date.year}{date.strftime('%m')}{date.strftime('%d')}.nc")
        files.extend(date_files)
    files.sort()

else:

    files = glob(f"{pathIn}/*/*.nc")
    files.sort()

for file in tqdm(files):
    filename = file.split("/")[-1].replace(".nc",".zarr")
    folder = file.split("/")[-2]
    if not os.path.exists(f"{pathIn}/{folder}/{filename}"):
        ds = xr.open_dataset(file)
        ds = ds.rename(dict(date="time"))
        ds = ds.drop(["n_neighbours","orbit","sat_track"])
        ds = ds.chunk(dict(time=-1,lon=-1,lat=-1))
        ds.to_zarr(f"{pathIn}/{folder}/{filename}")