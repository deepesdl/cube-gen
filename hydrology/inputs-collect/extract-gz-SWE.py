import gzip
import shutil
from glob import glob
from tqdm import tqdm
import os

pathOut = "~/data/hydrology/source/SWE_CPC_GPM_ERA5downT_RadGhent_filter5mm/"
pathOut = os.path.expanduser(pathOut)

files = glob(f"{pathOut}*.gz")
files.sort()

def extract_gz(file):

    filename = file.replace(".gz","")
    
    with gzip.open(file, 'rb') as f_in:
        with open(filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            
[extract_gz(file) for file in tqdm(files)]