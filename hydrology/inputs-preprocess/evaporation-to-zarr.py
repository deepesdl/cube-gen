import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os
from datetime import datetime, timedelta
import pandas as pd
from functools import partial


pathIn = f"~/data/hydrology/source/GLEAM_openloop_V1.1/"
pathIn = os.path.expanduser(pathIn)

files = glob(f"{pathIn}/*/*.nc")
files.sort()

for file in tqdm(files):
    filename = file.split("/")[-1].replace(".nc",".zarr")
    folder = file.split("/")[-2]
    if not os.path.exists(f"{pathIn}/{folder}/{filename}"):
        ds = xr.open_dataset(file)[["E"]]
        ds = ds.chunk(dict(time=64,lon=-1,lat=-1))
        ds.to_zarr(f"{pathIn}/{folder}/{filename}")