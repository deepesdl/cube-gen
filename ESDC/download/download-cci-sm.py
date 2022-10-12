import glob
from bs4 import BeautifulSoup
import requests
import xarray as xr
import rioxarray
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import numpy as np
import os

pathOut = "~/data-source/cci-sm/"

# if not os.path.exists(pathOut):
#     os.mkdir(pathOut)

def get_url_paths(url, ext='', params={}):
    response = requests.get(url, params=params)
    if response.ok:
        response_text = response.text
    else:
        return response.raise_for_status()
    soup = BeautifulSoup(response_text, 'html.parser')
    parent = [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
    return parent

def download_file(url):
    filename = url.split("/")[-1]
    pathFilename = f"{pathOut}/" + filename
    if not os.path.exists(pathFilename):
        response = requests.get(url,stream=True)
        print(response)
        if response.status_code == 200:
            with open(pathFilename, 'wb') as f:
                f.write(response.content)
    else:
        print(f"File {filename} already exists!")
    ds = xr.open_dataset(pathOut + "/ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-19790101000000-fv06.1.nc")
    ds = ds[['sm']].chunk(dict(time=1,lat=128,lon=128))
    ds.to_zarr(pathFilename.replace("nc","zarr"))
    os.remove(pathFilename)