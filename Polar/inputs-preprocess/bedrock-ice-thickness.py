import xarray as xr
import numpy as np
import rioxarray
import geopandas as gpd
import os
from glob import glob

pathIn = f"~/data/polar/source/bedrock_topography_and_geothermal_heat_flux_antarctica_goce"
pathIn = os.path.expanduser(pathIn)

pathOut = f"~/data/polar/cubes/bedrock_topography_and_geothermal_heat_flux_antarctica_goce"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)
    
filepath = os.path.join(pathIn,f'SMOS_IceThickness_2015_300.nc')

da = xr.open_dataset(filepath)
da = da.where(lambda x: x>0,other=np.nan)
da = da.sel(lat=slice(-90,-60))
da = da[["mrg"]].rio.write_crs(4326)
da = da.rename(dict(lon="x",lat="y"))
da = da.rio.reproject("EPSG:3031",nodata=np.nan)
da = da.chunk(dict(x=2048,y=2048))

da.to_zarr(f"{pathOut}/ice_thickness.zarr")