import calendar
import os
import numpy as np
from tqdm import tqdm

from utils import download_dataset_by_date

pathOut = "EO4SIBS-black-sea-chl"

if not os.path.exists(pathOut):
    os.mkdir(pathOut)

datasets = ["2016_l2_oc_chl", "2017_l2_oc_chl"]
months = np.arange(1, 13)

datasets_by_month = []

for year, dataset in enumerate(datasets, 2016):
    for month in months:
        if year == 2016:
            if month > 3:
                if month == 4:
                    datasets_by_month.append(
                        {
                            "start_date": "2016-04-26",
                            "end_date": f"{year}-{('0'+str(month))[-2:]}-{calendar.monthrange(year,month)[1]}",
                            "dataset": dataset,
                            "output_filename": f"{pathOut}/{dataset}_{('0'+str(month))[-2:]}.nc",
                        }
                    )
                elif month == 12:
                    datasets_by_month.append(
                        {
                            "start_date": f"{year}-{('0'+str(month))[-2:]}-01",
                            "end_date": f"{year}-{('0'+str(month))[-2:]}-30",
                            "dataset": dataset,
                            "output_filename": f"{pathOut}/{dataset}_{('0'+str(month))[-2:]}.nc",
                        }
                    )
                else:
                    datasets_by_month.append(
                        {
                            "start_date": f"{year}-{('0'+str(month))[-2:]}-01",
                            "end_date": f"{year}-{('0'+str(month))[-2:]}-{calendar.monthrange(year,month)[1]}",
                            "dataset": dataset,
                            "output_filename": f"{pathOut}/{dataset}_{('0'+str(month))[-2:]}.nc",
                        }
                    )
        else:
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
