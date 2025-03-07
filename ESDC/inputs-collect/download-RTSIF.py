import requests
import os
import patoolib
from tqdm import tqdm

### There is no native package for extracting .rar files
### 7-Zip or WinRAR are needed for extracting .rar files

url = "https://figshare.com/ndownloader/articles/19336346/versions/3"
filename = "cache.zip"
extract_path = "~/data/SIF/RTSIF/source"

zip_filename = os.path.join(extract_path, filename)

if not os.path.exists(extract_path):
    os.makedirs(extract_path)
    print("Extract path created.")

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

with open(zip_filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
) as progress_bar:
    for data in response.iter_content(chunk_size=1024):
        size = file.write(data)
        progress_bar.update(size)

print("File downloaded successfully.")

patoolib.extract_archive(zip_filename, outdir=extract_path)
print("Extraction completed.")

for filename in os.listdir(extract_path):
    if filename.endswith(".rar"):
        rar_file = os.path.join(extract_path, filename)
        patoolib.extract_archive(rar_file, outdir=extract_path)
        print(f"Extracted {filename} to {extract_path}")

for file in os.listdir(extract_path):
    file_path = os.path.join(extract_path, file)
    if file.endswith((".rar", ".zip")):
        os.remove(file_path)
        print(f"Deleted {file}")

print("All .rar and .zip files deleted.")
