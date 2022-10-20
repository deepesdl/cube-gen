import gzip
import shutil
import glob

from tqdm import tqdm

pathOut = "~/data/SIF/GOSIF/source"
pathOut = os.path.expanduser(pathOut)

files = glob.glob(f"{pathOut}/*")
files.sort()

for file in tqdm(files):
    with gzip.open(file, 'rb') as f_in:
        with open(file.replace(".gz",""), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)