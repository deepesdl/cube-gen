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

pathOut = "/net/projects/deep_esdl/data/MODIS/MCD43C4/data/"

if not os.path.exists(pathOut):
    os.mkdir(pathOut)
    
def get_dates_url_paths(url, ext='', params={}):
    response = requests.get(url, params=params)
    if response.ok:
        response_text = response.text
    else:
        return response.raise_for_status()
    soup = BeautifulSoup(response_text, 'html.parser')
    parent = [url + node.get('href') for node in soup.find_all('a') if node.get('href').startswith('20')]
    return parent

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
        if response.status_code == 200:
            with open(pathFilename, 'wb') as f:
                f.write(response.content)
    else:
        print(f"File {filename} already exists!")
        
days = get_dates_url_paths('https://e4ftl01.cr.usgs.gov/MOTA/MCD43C4.061/')

for day in tqdm(days):
    result = get_url_paths(day, 'hdf')
    download_file(result[0])