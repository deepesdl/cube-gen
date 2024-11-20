from typing import Any, Dict, List, Tuple, Union
from datetime import datetime
import collections
import warnings
import logging

import dask.array as da
import numpy as np
import pandas as pd
import xarray as xr
import dask

from xcube.core.gridmapping import GridMapping
from xcube.core.store import new_data_store

warnings.filterwarnings('ignore', r'All-NaN (slice|axis) encountered')

super_cube_fn = 'hydrology-1D-0.009deg-1x1102x966-1.0.0.levels'
root = "deep-esdl-output"
res = 0.009
data_store = new_data_store("s3", root=root)
base_datasets = list(data_store.get_data_ids())
base_datasets = [k for k in base_datasets if all(['hydrology-S' in k, '1D' in k])]


def get_geometry(ds):
    lat = ds.lat.values
    lon = ds.lon.values
    if lat[0] < lat[-1]:
        lat_min = lat[0]
        lat_max = lat[-1]
    else:
        lat_min = lat[-1]
        lat_max = lat[0]
    if lon[0] < lon[-1]:
        lon_min = lon[0]
        lon_max = lon[-1]
    else:
        lon_min = lon[-1]
        lon_max = lon[0]
    spatial_res_lat = np.diff(lat)
    spatial_res_lon = np.diff(lon)
    if not np.all(np.isclose(np.diff(spatial_res_lat), 0)):
         raise ValueError("Lat res is not constant.")
    if not np.all(np.isclose(np.diff(spatial_res_lon), 0)):
         raise ValueError("Lon res is not constant.")
    return [lon_min, lat_min, lon_max, lat_max] , (spatial_res_lon[0], spatial_res_lat[0]), (len(lon), len(lat))

def get_sub_cube_infos(data_store, base_datasets):
    sub_cubes = []
    for base_id in base_datasets:
        ds = data_store.open_data(base_id)
        xy_bbox, xy_res, size = get_geometry(ds)
        time_span = (ds.time.values[0], ds.time.values[-1])
        sub_cubes.append(SubCubeInfo(base_id, xy_bbox, xy_res, None, size, time_span))
        ds.close()
    return sub_cubes

SubCubeInfo = collections.namedtuple("SubCubeInfo",
                       ["base_id",
                        "xy_bbox",
                        "xy_res",
                        "ij_bbox",
                        "size",
                        "time_span"])
sub_cubes = get_sub_cube_infos(data_store, base_datasets)

# find overall bounds:
# bbox
uber_lon_min = min([sub_cube.xy_bbox[0] for sub_cube in sub_cubes])
uber_lat_min = min([sub_cube.xy_bbox[1] for sub_cube in sub_cubes])
uber_lon_max = max([sub_cube.xy_bbox[2] for sub_cube in sub_cubes])
uber_lat_max = max([sub_cube.xy_bbox[3] for sub_cube in sub_cubes])

# time:
uber_time_min = min([sub_cube.time_span[0] for sub_cube in sub_cubes])
uber_time_max = max([sub_cube.time_span[1] for sub_cube in sub_cubes])

sub_cubes2 = []
for sub_cube in sub_cubes:
    x1, y1, x2, y2 = sub_cube.xy_bbox
    i1 = (x1 - uber_lon_min) / res
    j1 = (y1 - uber_lat_min) / res
    i2 = (x2 - uber_lon_min) / res
    j2 = (y2 - uber_lat_min) / res
    sub_cube2 = sub_cube._replace(ij_bbox = list(map(round, [i1, j1, i2, j2])))
    sub_cubes2.append(sub_cube2)

sub_cubes = sub_cubes2

i_min = min([sub_cube.ij_bbox[0] for sub_cube in sub_cubes])
j_min = min([sub_cube.ij_bbox[1] for sub_cube in sub_cubes])
i_max = max([sub_cube.ij_bbox[2] for sub_cube in sub_cubes])
j_max = max([sub_cube.ij_bbox[3] for sub_cube in sub_cubes])

uber_bbox = (uber_lon_min, uber_lat_min, uber_lon_max, uber_lat_max)
uber_lat_bnds = (uber_lat_min - res,
                 uber_lat_max + res)
uber_lon_bnds = (uber_lon_min - res,
                 uber_lon_max + res)

uber_times = pd.date_range(uber_time_min, uber_time_max, freq='1D')

ds_template = data_store.open_data(base_datasets[0])

data_vars = []
for var_name, var  in ds_template.data_vars.items():
    data_vars.append((var_name, var.dtype, var.encoding["_FillValue"], var.attrs))

wanted = ['Conventions',
          'acknowledgment',
          'contributor_name',
          'contributor_url',
          'creator_name',
          'creator_url',
          'license',
          'project',
          'publisher_name',
          'publisher_url']

global_attrs = {k:v for k,v in ds_template.attrs.items() if k in wanted}

xy_res = 0.009
width = i_max  # pixels
height = j_max  # pixels

tile_size = width, height  # no spatial chunks!

xy_min = uber_lon_min - xy_res / 2, uber_lat_min - xy_res / 2

super_cube_gm = GridMapping.regular(size=(width, height),
                                    xy_min=xy_min,
                                    xy_res=xy_res,
                                    tile_size=tile_size,
                                    crs="OGC:CRS84",
                                    is_j_axis_up=False)
def new_super_cube_template(
    gm: GridMapping,
    data_vars: Tuple[str, np.dtype, Union[int, float], Dict[str, Any]],
    global_attrs: Dict[str, Any],
    time: np.ndarray,
    time_chunk_size: int = 1,
):
    time_name = "time"
    x_name, y_name = gm.xy_dim_names
    width, height = gm.size
    tile_width, tile_height = gm.tile_size
    spatial_coords = gm.to_coords()

    data_var_dims = time_name, y_name, x_name
    data_var_shape = len(time), height, width
    data_var_chunks = time_chunk_size, tile_height, tile_width

    return xr.Dataset(
        data_vars=dict(
            **{name: xr.DataArray(da.full(data_var_shape,
                                          fill_value,
                                          chunks=data_var_chunks,
                                          dtype=dtype,
                                          name=f'{name}_base'),
                                  dims=data_var_dims,
                                  attrs=attrs)
               for name, dtype, fill_value, attrs in data_vars},
        ),
        coords=dict(
            **spatial_coords,
            time=xr.DataArray(time,
                              dims="time"),

        ),
        attrs= global_attrs
    )

super_cube_template = new_super_cube_template(
    super_cube_gm,
    data_vars,
    global_attrs,
    uber_times,
    time_chunk_size=1
)

region_paths = [sub_cube.base_id for sub_cube in sub_cubes]
region_xy_bboxes = np.array([sub_cube.xy_bbox for sub_cube in sub_cubes])
region_ij_bboxes = np.array([sub_cube.ij_bbox for sub_cube in sub_cubes])


def block_mapper(block_ds: xr.Dataset,
                 ds_time_index: pd.DatetimeIndex,
                 region_paths: List[str],
                 region_ij_bboxes: np.ndarray):
    from dask.distributed import print

    # Assuming time chunking = 1
    time = block_ds.time.values[0]
    time_idx = ds_time_index.get_loc(time)

    width = block_ds.dims["lon"]
    height = block_ds.dims["lat"]

    time_tolerance = pd.Timedelta("12H")

    target_arrays = {var_name: block_var.values
                     for var_name, block_var in block_ds.data_vars.items()}
    data_store = new_data_store("s3",
                                root="deep-esdl-output/alicja-hydro-testing")
    for region_path, region_ij_bbox in zip(region_paths, region_ij_bboxes):
        # print(f'Processing {region_path}, region {region_ij_bbox}, time={time}', flush=True)
        i1, j1, _, _ = region_ij_bbox
        sub_cube = data_store.open_data(region_path)
        sub_cube_start = sub_cube.time[0]
        sub_cube_stop = sub_cube.time[-1]
        if time > sub_cube_start - time_tolerance \
                and time < sub_cube_stop + time_tolerance:
            sub_cube_slice = sub_cube.sel(time=time, method="nearest")
            for var_name, block_var in block_ds.data_vars.items():
                target_array = target_arrays.get(var_name)
                source_array = sub_cube_slice[var_name].values
                # print(f'copy source of shape {source_array.shape} into target of shape {target_array.shape}, region {region_ij_bbox}')
                source_h, source_w = source_array.shape
                i2 = min(i1 + source_w, width)
                j2 = min(j1 + source_h, height)
                source_w = i2 - i1
                source_h = j2 - j1
                interm_array = np.copy(
                    block_var.values)  # block_var.values is read-only
                interm_array[0, j1:j2, i1:i2] = source_array[0:source_h,
                                                0:source_w][::-1, :]
                target_array = np.nanmax(
                    np.stack([target_array, interm_array]), axis=0)
                target_arrays[var_name] = target_array
        sub_cube.close()

    block_ds = block_ds.copy()
    for var_name, target_array in target_arrays.items():
        var = block_ds[var_name]
        block_ds[var_name] = xr.DataArray(target_array[:, ::-1, :],
                                          dims=var.dims, attrs=var.attrs)

    print(
        f'Processed {len(region_paths)} dataset slices for time={time}, index={time_idx}',
        flush=True)

    return block_ds

super_cube = super_cube_template.map_blocks(
    block_mapper,
    args=[super_cube_template.get_index("time"),
          region_paths,
          region_ij_bboxes],
    template=super_cube_template
)

super_cube.attrs["title"] = "Hydrology Cube"
super_cube.SM.attrs["processing_steps"] = ['Gridding nc datasets', 'daily aggregates']
encoding_dict = dict()

coords_encoding = {k: dict(chunks=None) for k, v in super_cube.coords.items()}
vars_encoding = {k: dict(write_empty_chunks=False,
                         chunks=(1,1102,966),
                         dtype=np.dtype('float32'))
                 for k, v in super_cube.data_vars.items()}

encoding_dict.update(coords_encoding)
encoding_dict.update(vars_encoding)

dask.config.set({'logging.distributed': 'error'})

start_run_time = datetime.now()
print(f'{start_run_time} Starting to persist final cube. This will take some time.')

data_store.write_data(super_cube,
                      super_cube_fn,
                      encoding=encoding_dict,
                      replace=True,
                      num_levels=5,
                      use_saved_levels=True)
print(f'Took:  {datetime.now() - start_run_time}')
print(f'Final cube persisted.')