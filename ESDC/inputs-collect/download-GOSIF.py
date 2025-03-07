from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import re
import os
from os.path import exists

URL = "http://data.globalecology.unh.edu/data/GOSIF_v2/8day/"
# pathOut = "/net/projects/deep_esdl/data/GOSIF/data/"

pathOut = "~/data/SIF/GOSIF/source"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)

req = Request(URL)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []

for link in soup.findAll('a'):
    link = link.get('href')
    if link.endswith(".tif.gz"):
        file_to_download = link.split("/")[-1]
        file_path = os.path.join(pathOut, file_to_download)
        if not exists(file_path):
            print(f"Downloading {file_to_download}")
            response = requests.get(URL + file_to_download)
            open(file_path, "wb").write(response.content)
        else:
            pass
