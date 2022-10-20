import xarray as xr
import numpy as np
import glob
import os

from tqdm import tqdm

pathIn = "path-to-hourly-ERA5-data"

pathOut = "~/data/ERA5/preprocess/monthly"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)

# pathOut = "/Net/Groups/BGI/work_1/scratch/dmontero/ERA5/monthly"

# if not os.path.exists(pathOut):
#     os.mkdir(pathOut)
    
years=np.arange(1979,2022)
months=[("0"+str(x))[-2:] for x in np.arange(1,13)]

for year in years:
    print(f"Working on {year}...")
    for month in tqdm(months):
        if not os.path.exists(f"{pathOut}/era5-{year}-{month}.zarr"):
            e=xr.open_dataset(glob.glob(f"{pathIn}/e/{year}/e.hh.*.era5.{month}.{year}.nc")[0])
            tp=xr.open_dataset(glob.glob(f"{pathIn}/tp/{year}/tp.hh.*.era5.{month}.{year}.nc")[0])
            t2m=xr.open_dataset(glob.glob(f"{pathIn}/t2m/{year}/t2m.hh.*.era5.{month}.{year}.nc")[0])
            ssr=xr.open_dataset(glob.glob(f"{pathIn}/ssr/{year}/ssr.hh.*.era5.{month}.{year}.nc")[0])

            e=e.resample(time="1D").sum()*1000
            tp=tp.resample(time="1D").sum()*1000
            t2m_max=t2m.resample(time="1D").max()-273.15
            t2m_min=t2m.resample(time="1D").min()-273.15
            t2m=t2m.resample(time="1D").mean()-273.15
            ssr=ssr.resample(time="1D").mean()

            t2m_max=t2m_max.rename({'t2m':'t2m_max'})
            t2m_min=t2m_min.rename({'t2m':'t2m_min'})

            ds=xr.merge([e,tp,t2m,t2m_max,t2m_min,ssr])

            ds.coords['longitude'] = (ds.coords['longitude'] + 180) % 360 - 180
            ds=ds.sortby(ds.longitude)
            ds=ds.rename(dict(longitude='lon',latitude='lat'))

            ds=ds.chunk(dict(time=-1,lat=256,lon=256))

            ds.to_zarr(f"{pathOut}/era5-{year}-{month}.zarr")
            

print("Done!")