import requests
import numpy as np

URL = "http://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/ECOCLIM/Downscaled-GOME2-SIF/v2.0/"
# pathOut = "/net/projects/deep_esdl/data/GOME2-SIF/data/"

pathOut = "~/data/SIF/GOME2-SIF/source"
pathOut = os.path.expanduser(pathOut)

if not os.path.exists(pathOut):
    os.makedirs(pathOut)

retrieval_methods = ["JJ", "PK"]
years = np.arange(2007,2019)

for rm in retrieval_methods:
    for year in years:
        file_to_download = f"GOME_{rm}_dcSIF_005deg_8day_{year}.nc"
        print(f"Downloading {file_to_download}")
        response = requests.get(URL + file_to_download)
        open(pathOut + file_to_download, "wb").write(response.content)