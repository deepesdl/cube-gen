import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
import os
from datetime import datetime, timedelta
import pandas as pd
from functools import partial


pathIn = f"~/data/hydrology/source/precipitation_GPM_CPC_SM2RAIN-ASCAT/"
pathIn = os.path.expanduser(pathIn)

files = glob(f"{pathIn}/*.nc")
files.sort()

for file in tqdm(files):
    filename = file.split("/")[-1].replace(".nc",".zarr")
    if not os.path.exists(f"{pathIn}{filename}"):
        ds = xr.open_dataset(file)
        ds = ds.chunk(dict(time=128,lon=-1,lat=-1))
        ds.to_zarr(f"{pathIn}{filename}")