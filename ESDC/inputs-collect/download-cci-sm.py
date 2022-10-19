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

pathOut = "/net/scratch/dmontero/CCI/SM"

if not os.path.exists(pathOut):
    os.mkdir(pathOut)

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
    if not os.path.exists(pathFilename.replace("nc","zarr")):
        response = requests.get(url,stream=True)
        if response.status_code == 200:
            with open(pathFilename, 'wb') as f:
                f.write(response.content)
        ds = xr.open_dataset(pathFilename)
        ds = ds[['sm']].chunk(dict(time=1,lat=128,lon=128))
        ds.to_zarr(pathFilename.replace("nc","zarr"))
        os.remove(pathFilename)
    else:
        print(f"File {filename} already exists!")

years = np.arange(1979,2021)

for year in tqdm(years):
    urls = get_url_paths(f"https://dap.ceda.ac.uk/neodc/esacci/soil_moisture/data/daily_files/COMBINED/v06.1/{year}/","nc")
    for url in urls:
        download_file(url)
