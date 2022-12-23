import xarray as xr
import numpy as np
import rioxarray
import geopandas as gpd
import os
from glob import glob

pathIn = "~/data/polar/source/repeat_subglacial_lake_drainage_and_filling_thwaites_glacier"
pathIn = os.path.expanduser(pathIn)

pathOut = "~/data/polar/cubes/repeat_subglacial_lake_drainage_and_filling_thwaites_glacier"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)
    
lakes = [70,124,142,170]

def to_xarray(da,lake,year):
    da = da.isel(band=0).drop("band")
    da.attrs = dict()
    da.name = f"Thw_{lake}"
    da = da.assign_coords(dict(time=np.datetime64(f"{year}-01-01"))).expand_dims("time")
    da = da.to_dataset()
    da = da.where(lambda x: x > 0,other=np.nan)
    return da

da_lakes = []

for lake in lakes:
    
    lake_path_2013 = os.path.join(pathIn,f'Thw{lake}_2013_mask.tif')
    lake_path_2017 = os.path.join(pathIn,f'Thw{lake}_2017_mask.tif')
    
    da_2013 = to_xarray(rioxarray.open_rasterio(lake_path_2013),lake,2013)
    da_2017 = to_xarray(rioxarray.open_rasterio(lake_path_2017),lake,2017)
    
    da = xr.concat([da_2013,da_2017],dim="time")
    
    da_lakes.append(da)
    
da = xr.merge(da_lakes)
da = da.chunk()

da.to_zarr(f"{pathOut}/thwaites_sublacial_lakes_2013_2017.zarr")