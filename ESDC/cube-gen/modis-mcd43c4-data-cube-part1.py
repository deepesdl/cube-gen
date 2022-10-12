import xarray as xr
import rioxarray
import numpy as np
import glob
import os
import datetime
from tqdm import tqdm

files = glob.glob("/net/projects/deep_esdl/data/MODIS/MCD43C4/data/*.hdf")
files.sort()

chunks = dict(band=1,y=512,x=512)

variables = {
    'Nadir_Reflectance_Band1': 'float32',
    'Percent_Inputs': 'int8',
    'Percent_Snow': 'int8',
    'BRDF_Albedo_Uncertainty': 'float32',
    'Nadir_Reflectance_Band2': 'float32',
    'Nadir_Reflectance_Band3': 'float32',
    'Nadir_Reflectance_Band4': 'float32',
    'Nadir_Reflectance_Band5': 'float32',
    'Nadir_Reflectance_Band6': 'float32',
    'Nadir_Reflectance_Band7': 'float32',
    'Albedo_Quality': 'int8',
    'Local_Solar_Noon': 'int8'
}

def read_and_chunk(file):

    filename = file.split("/")[-1]
    date = filename.split(".")[1][1:]
    date = np.datetime64(datetime.datetime.strptime(date, '%Y%j'))

    ds = rioxarray.open_rasterio(file,chunks=chunks).sel(band=1).drop("band")

    for variable, datatype in variables.items():
        fill = ds[variable].attrs['_FillValue']
        scale = ds[variable].attrs['scale_factor']
        offset = ds[variable].attrs['add_offset']
        ds[variable] = ((ds[variable].where(lambda x: x != fill,other = np.nan) * scale) + offset).astype(datatype)

    ds['x'] = np.arange(-179.975,180,0.05)
    ds['y'] = np.arange(89.975,-90,-0.05)

    ds = ds.rename({"y": "lat", "x":"lon"})
    ds = ds.assign_coords({"time": date}).expand_dims("time")
    ds = ds.transpose("time","lat","lon")
    ds.to_zarr(f"/net/projects/deep_esdl/data/MODIS/MCD43C4/data/{filename.replace('.hdf','.zarr')}")

[read_and_chunk(file) for file in tqdm(files)]