import json
import requests
import os
import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup

SOURCES_TO_DOWNLOAD = ["Particulate Organic Carbon", "Particulate Inorganic Carbon"]

pathOut = "~/data/ocean/source/"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)

with open('../cube9km.geojson', 'r') as f:
    cube_specs = json.load(f)

def list_files_nc(url, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]

def download_file(source):
    if source["name"] in SOURCES_TO_DOWNLOAD:
        print(f"Downloading {source}")
        output_source_path = pathOut + "/" + source['name'].lower().replace(" ","_")
        if not os.path.exists(output_source_path):
            os.makedirs(output_source_path)
        url = source['download_url']
        files = list_files_nc(url, "nc")
        print(f"Retrieving and downloading files...")
        for file in tqdm(files):
            filename = file
            output = output_source_path + "/" + filename
            r = requests.get(f"{url}{file}")
            if r.status_code == 200:
                if not os.path.exists(output):
                    open(output, "wb").write(r.content)

[download_file(source) for source in cube_specs['properties']['sources']]
