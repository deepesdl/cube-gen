import requests
import calendar
import os
import numpy as np
from tqdm import tqdm

from utils import download_dataset_by_date

pathOut = "EO4SIBS-black-sea-altimetry"

if not os.path.exists(pathOut):
    os.mkdir(pathOut)

datasets = ["2016_l4_altimetry", "2017_l4_altimetry"]
months = np.arange(1, 13)

datasets_by_month = []

for year, dataset in enumerate(datasets, 2016):
    for month in months:
        datasets_by_month.append(
            {
                "start_date": f"{year}-{('0'+str(month))[-2:]}-01",
                "end_date": f"{year}-{('0'+str(month))[-2:]}-{calendar.monthrange(year,month)[1]}",
                "dataset": dataset,
                "output_filename": f"{pathOut}/{dataset}_{('0'+str(month))[-2:]}.nc",
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
