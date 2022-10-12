import gzip
import shutil
import glob

from tqdm import tqdm

files = glob.glob("/net/projects/deep_esdl/data/GOSIF/data/*")
files.sort()

for file in tqdm(files):
    with gzip.open(file, 'rb') as f_in:
        with open(file.replace(".gz",""), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)