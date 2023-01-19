import xarray as xr
import numpy as np
import rioxarray
import geopandas as gpd
import os
from glob import glob
import json

with open('../cube.geojson', 'r') as f:
    cube_specs = json.load(f)

bbox = cube_specs['properties']['spatial_bbox']
step = cube_specs['properties']['spatial_res']

x = np.arange(bbox[0],bbox[2],step[0]) + step[0]/2
y = np.arange(bbox[1],bbox[3],step[1]) + step[1]/2

ref_spatial = dict(x=x,y=y)

for size in [200,300]:

    pathOut = f"~/data/polar/cubes/geothermal_heat_flow_{size}x{size}km_xyz_data"
    pathOut = os.path.expanduser(pathOut)

    filepath = f"{pathOut}/geothermal_heat_flow_{size}km.zarr"

    da = xr.open_zarr(filepath)
    da = da.interp(ref_spatial,method="linear")
    da = da.chunk(dict(x=2048,y=2048))

    filename = filepath.split("/")[-1].replace(".zarr","_100m.zarr")

    da.to_zarr(f"{pathOut}/{filename}")
