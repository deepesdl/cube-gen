from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import re
from os.path import exists

URL = "http://data.globalecology.unh.edu/data/GOSIF_v2/8day/"
PATH = "/net/projects/deep_esdl/data/GOSIF/data/"

req = Request(URL)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []

for link in soup.findAll('a'):
    link = link.get('href')
    if link.endswith(".tif.gz"):
        file_to_download = link.split("/")[-1]
        if not exists(PATH + file_to_download):
            print(f"Downloading {file_to_download}")
            response = requests.get(URL + file_to_download)
            open(PATH + file_to_download, "wb").write(response.content)
        else:
            pass