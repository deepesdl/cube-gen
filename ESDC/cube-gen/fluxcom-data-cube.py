import xarray as xr
import numpy as np
import glob

from tqdm import tqdm

print("Reading")
Cpath="/Net/Groups/BGI/work_3/FluxcomDataStructure/internal/QOVbZtjf6sSIZowqIc99/tCarbonFluxes/RS_V006/ensemble/4320_2160/8daily"
Epath="/Net/Groups/BGI/work_3/FluxcomDataStructure/internal/QOVbZtjf6sSIZowqIc99/tEnergyFluxes/RS_V006/ensemble/4320_2160/8daily"

GPPfiles=glob.glob(f"{Cpath}/GPP*.nc")
GPPfiles.sort()

NEEfiles=glob.glob(f"{Cpath}/NEE*.nc")
NEEfiles.sort()

TERfiles=glob.glob(f"{Cpath}/TER*.nc")
TERfiles.sort()

Hfiles=glob.glob(f"{Epath}/H*.nc")
Hfiles.sort()

LEfiles=glob.glob(f"{Epath}/LE*EBC-ALL*.nc")
LEfiles.sort()

Rnfiles=glob.glob(f"{Epath}/Rn*.nc")
Rnfiles.sort()

def merge_datasets(i):
    gpp = xr.open_dataset(GPPfiles[i],chunks=dict(time=-1,lat=256,lon=256))[['GPP']]
    nee = xr.open_dataset(NEEfiles[i],chunks=dict(time=-1,lat=256,lon=256))[['NEE']]
    ter = xr.open_dataset(TERfiles[i],chunks=dict(time=-1,lat=256,lon=256))[['TER']]
    h = xr.open_dataset(Hfiles[i],chunks=dict(time=-1,lat=256,lon=256))[['H']]
    le = xr.open_dataset(LEfiles[i],chunks=dict(time=-1,lat=256,lon=256))[['LE']]
    rn = xr.open_dataset(Rnfiles[i],chunks=dict(time=-1,lat=256,lon=256))[['Rn']]
    return xr.merge([gpp,nee,ter,h,le,rn])

print("Merging")
fluxcom = xr.concat([merge_datasets(i) for i in tqdm(np.arange(0,20))],dim="time")

fluxcom['time'] = fluxcom.time + np.timedelta64(4,"D")

fluxcom = fluxcom.chunk(dict(time=256,lat=256,lon=256))

print("Saving")
fluxcom.to_zarr("/Net/Groups/BGI/work_1/scratch/dmontero/FLUXCOM/fluxcom-8d-0.083deg-256x256x256.zarr")