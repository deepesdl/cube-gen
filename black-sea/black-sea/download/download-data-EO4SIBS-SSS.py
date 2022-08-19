import requests
import calendar
import os
import numpy as np
from tqdm import tqdm

from utils import download_dataset_by_date

pathOut = "EO4SIBS-black-sea-sss"

if not os.path.exists(pathOut):
    os.mkdir(pathOut)

dataset = "sss_l3_v3"
years = [2016, 2017]
months = np.arange(1, 13)

datasets_by_month = []

for year in years:
    for month in months:
        datasets_by_month.append(
            {
                "start_date": f"{year}-{('0'+str(month))[-2:]}-01",
                "end_date": f"{year}-{('0'+str(month))[-2:]}-{calendar.monthrange(year,month)[1]}",
                "dataset": dataset,
                "output_filename": f"{pathOut}/{dataset}_{year}_{('0'+str(month))[-2:]}.nc",
            }
        )

datasets_by_month = [
    x for x in datasets_by_month if not os.path.exists(x["output_filename"])
]

for dataset_by_month in tqdm(datasets_by_month):
    download_dataset_by_date(
        dataset_by_month["dataset"],
        dataset_by_month["start_date"],
        dataset_by_month["end_date"],
        dataset_by_month["output_filename"],
    )
