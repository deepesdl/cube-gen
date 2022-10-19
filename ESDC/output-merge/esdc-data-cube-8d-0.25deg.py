from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

import shapely.geometry
from IPython.display import JSON
import matplotlib.pyplot as plt

import xarray as xr
import numpy as np

from datetime import datetime
import yaml

def remove_attr(dictionary,attr):
    if attr in dictionary.keys():
        del dictionary[attr]
        
def remove_attrs(dictionary,attrs):
    [remove_attr(dictionary,attr) for attr in attrs]
    
def remove_attrs_dataset(ds,variables,attrs):
    for variable in variables:
        remove_attrs(ds[variable].attrs,attrs)
    
def combine_attrs_variable(global_attrs,local_attrs):
    for key, value in global_attrs.items():
        if key in local_attrs.keys():
            if not isinstance(local_attrs[key],list):
                local_attrs[key] = [local_attrs[key]]
            if not isinstance(value,list):
                value = [value]
            [local_attrs[key].append(val) for val in value if val not in local_attrs[key]]
            # local_attrs[key]=local_attrs[key] + value
        else:
            local_attrs[key]=value
        
def combine_attrs_dataset(ds,variables):
    for variable in variables:
        combine_attrs_variable(ds.attrs,ds[variable].attrs)
        
def rename_and_add_attr(ds,rename_dict):
    ds=ds.rename(rename_dict)
    for original_name, new_name in rename_dict.items():
        ds[new_name].attrs['original_name']=original_name
    return ds

def rearrange_dataset(ds,rename_dict):
    combine_attrs_dataset(ds,rename_dict.keys())
    remove_attrs_dataset(ds,rename_dict.keys(),[
        'grid_mapping',
        'id',
        'Conventions',
        'add_offset',
        'scale_factor'
    ])
    ds=rename_and_add_attr(ds,rename_dict)
    ds=ds.drop("crs")
    return ds

def round_coords(ds):
    ds['lat'] = ds.lat.round(3)
    ds['lon'] = ds.lon.round(3)
    return ds

print("Reading and rearranging")
store = new_data_store("s3", root="deep-esdl-input")
store_output = new_data_store("s3", root="deep-esdl-output")

fluxcom = store.open_data('fluxcom-8d-0.25deg-256x128x128.zarr')

rename_dict={
    "GPP": "gross_primary_productivity",
    "NEE": "net_ecosystem_exchange",
    "TER": "terrestrial_ecosystem_respiration",
    "H": "sensible_heat",
    "LE": "latent_energy",
    "Rn": "net_radiation"
}

fluxcom = rearrange_dataset(fluxcom,rename_dict)
fluxcom = round_coords(fluxcom)

modis = store.open_data('modis-mcd43c4-vis-mask-8d-0.25deg-256x128x128.zarr')

rename_dict={
    "Nadir_Reflectance_Band1": "nbar_red",
    "Nadir_Reflectance_Band2": "nbar_nir",
    "Nadir_Reflectance_Band3": "nbar_blue",
    "Nadir_Reflectance_Band4": "nbar_green",
    "Nadir_Reflectance_Band5": "nbar_swir1",
    "Nadir_Reflectance_Band6": "nbar_swir2",
    "Nadir_Reflectance_Band7": "nbar_swir3",
    "NDVI": "ndvi",
    "kNDVI": "kndvi",
    "NIRv": "nirv"
}

modis = rearrange_dataset(modis,rename_dict)
modis=round_coords(modis)

aod = store.open_data('cci-aod550-8d-0.25deg-256x128x128.zarr')

rename_dict={
    "AOD550_mean": "aerosol_optical_thickness_550"
}

aod = rearrange_dataset(aod,rename_dict)

cloud = store.open_data('cci-cloud-8d-0.25deg-256x128x128.zarr')

rename_dict={
    "cot": "cot",
    "cth": "cth",
    "ctt": "ctt"
}

cloud = rearrange_dataset(cloud,rename_dict)

sm = store.open_data('cci-sm-8d-0.25deg-256x128x128.zarr')

rename_dict={
    "sm": "sm"
}

sm = rearrange_dataset(sm,rename_dict)

era5 = store.open_data('era5-8d-0.25deg-256x128x128.zarr')

rename_dict={
    "e": "evaporation_era5",
    "ssr": "radiation_era5",
    "t2m": "air_temperature_2m",
    "t2m_max": "max_air_temperature_2m",
    "t2m_min": "min_air_temperature_2m",
    "tp": "precipitation_era5",
}

era5 = rearrange_dataset(era5,rename_dict)
era5['time'] = era5.time + np.timedelta64(4,"D")

gfed4 = store.open_data('gfed4-burntarea-8d-0.25deg-256x128x128.zarr')

rename_dict={
    "burnt_area": "burnt_area"
}

gfed4 = rearrange_dataset(gfed4,rename_dict)

sifgome2jj = store.open_data('sif-gome2-JJ-8d-0.25deg-256x128x128.zarr')

rename_dict={
    "SIF": "sif_gome2_jj"
}

sifgome2jj = rearrange_dataset(sifgome2jj,rename_dict)
sifgome2jj=round_coords(sifgome2jj)

sifgome2pk = store.open_data('sif-gome2-PK-8d-0.25deg-256x128x128.zarr')

rename_dict={
    "SIF": "sif_gome2_pk"
}

sifgome2pk = rearrange_dataset(sifgome2pk,rename_dict)
sifgome2pk=round_coords(sifgome2pk)

gosif = store.open_data('sif-gosif-8d-0.25deg-256x128x128.zarr')

rename_dict={
    "sif": "sif_gosif"
}

gosif = rearrange_dataset(gosif,rename_dict)
gosif=round_coords(gosif)

rtsif = store.open_data('sif-rtsif-8d-0.25deg-256x128x128.zarr')

rename_dict={
    "sif": "sif_rtsif"
}

rtsif = rearrange_dataset(rtsif,rename_dict)
rtsif=round_coords(rtsif)

gleam = store.open_data('gleam-8d-0.25deg-256x128x128.zarr')

rename_dict={
    "E": "evaporation",
    "Eb": "bare_soil_evaporation",
    "Ei": "interception_loss",
    "Ep": "potential_evaporation",
    "Es": "snow_sublimation",
    "Et": "transpiration",
    "Ew": "open_water_evaporation",
    "S": "evaporative_stress",
    "SMroot": "root_moisture",
    "SMsurf": "surface_moisture"    
}

gleam = rearrange_dataset(gleam,rename_dict)

print("Merging")
datacube = xr.merge([
    fluxcom,
    modis,
    aod,
    cloud,
    sm,
    era5,
    gfed4,
    sifgome2jj,
    sifgome2pk,
    gosif,
    rtsif,
    gleam
])

print("Adding new variables")
with open("esdc-metadata.yaml", "r") as stream:
    try:
        metadata = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

datacube.attrs = metadata["global"]

additional_attrs = {
    "date_modified": str(datetime.now()),
    "geospatial_lat_max": float(datacube.lat.max().values),
    "geospatial_lat_min": float(datacube.lat.min().values),
    "geospatial_lat_resolution": float(
        datacube.lat[1] - datacube.lat[0]
    ),
    "geospatial_lon_max": float(datacube.lon.max().values),
    "geospatial_lon_min": float(datacube.lon.min().values),
    "geospatial_lon_resolution": float(
        datacube.lon[1] - datacube.lon[0]
    ),
    "time_coverage_start": str(datacube.time[0].values),
    "time_coverage_end": str(datacube.time[-1].values),
}

datacube.attrs = dict(
    sorted({**datacube.attrs, **additional_attrs}.items())
)

print("Chunking")
datacube = datacube.chunk(dict(time=256,lat=128,lon=128))

for variable in datacube.variables.keys():
    if 'chunks' in datacube[variable].encoding.keys():
        del datacube[variable].encoding['chunks']

print("Saving")
store_output.write_data(
    datacube, 'esdc-8d-0.25deg-256x128x128-3.0.0.zarr', replace=True
)