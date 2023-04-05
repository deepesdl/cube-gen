import json
import requests
import os
import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup

SOURCES_TO_DOWNLOAD = [
    "Monthly global Oceanic Export Production",
    "Monthly global Marine Phytoplankton Primary Production"
]

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
        years = np.arange(1997,2021)
        files = []
        print(f"Retrieving files...")
        for year in tqdm(years):
            r = requests.get(f"{url}{year}")
            if r.status_code == 200:
                files.extend(list_files_nc(f"{url}{year}/","download=1"))
        files = np.unique(files).tolist()
        print(f"Downloading files...")
        for file in tqdm(files):
            filename = file.replace("?download=1","").split("/")[-1]
            output = output_source_path + "/" + filename
            if not os.path.exists(output):
                response = requests.get(file)        
                open(output, "wb").write(response.content)
        
[download_file(source) for source in cube_specs['properties']['sources']]