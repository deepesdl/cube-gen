import json
import requests
import tarfile
import zipfile
import getpass
import os
from tqdm import tqdm

pathOut = "~/data/polar/source/"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)
    
with open('cube.geojson', 'r') as f:
    cube_specs = json.load(f)
    
def download_file(source):
    output_source_path = pathOut + "/" + source['name'].lower().replace(" ","_")
    if not os.path.exists(output_source_path):
        os.makedirs(output_source_path)
    url = source['download_url']
    filename = url.split("/")[-1]
    if source['credentials']:
        user = getpass.getpass("username:")
        password = getpass.getpass("password")
        response = requests.get(url,auth=(user,password))
    else:
        response = requests.get(url)
    output = output_source_path + "/" + filename
    open(output, "wb").write(response.content)
    if source['compressed']:
        if source['compression_format'] == 'tar':
            tar = tarfile.open(output, "r:")
            tar.extractall()
            tar.close()
        elif source['compression_format'] == 'zip':
            with zipfile.ZipFile(output,"r") as zip_ref:
                zip_ref.extractall()
                
[download_file(source) for source in tqdm(cube_specs['properties']['sources'])]