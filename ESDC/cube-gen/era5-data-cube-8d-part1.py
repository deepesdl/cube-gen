import xarray as xr
import numpy as np
import glob
import os

from tqdm import tqdm

pathOut = "/Net/Groups/BGI/work_1/scratch/dmontero/ERA5/monthly"

if not os.path.exists(pathOut):
    os.mkdir(pathOut)
    
years=np.arange(1979,2022)
months=[("0"+str(x))[-2:] for x in np.arange(1,13)]

for year in years:
    print(f"Working on {year}...")
    for month in tqdm(months):
        if not os.path.exists(f"{pathOut}/era5-{year}-{month}.zarr"):
            e=xr.open_dataset(glob.glob(f"/Net/Groups/data_BGC/era5/e1/0d25_hourly/e/{year}/e.hh.*.era5.{month}.{year}.nc")[0])
            tp=xr.open_dataset(glob.glob(f"/Net/Groups/data_BGC/era5/e1/0d25_hourly/tp/{year}/tp.hh.*.era5.{month}.{year}.nc")[0])
            t2m=xr.open_dataset(glob.glob(f"/Net/Groups/data_BGC/era5/e1/0d25_hourly/t2m/{year}/t2m.hh.*.era5.{month}.{year}.nc")[0])
            ssr=xr.open_dataset(glob.glob(f"/Net/Groups/data_BGC/era5/e1/0d25_hourly/ssr/{year}/ssr.hh.*.era5.{month}.{year}.nc")[0])

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