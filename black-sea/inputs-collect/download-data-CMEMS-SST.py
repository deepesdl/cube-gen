import ftplib
import numpy as np
from tqdm import tqdm
from getpass import getpass

pathOut = "CMEMS-black-sea-sst"

if not os.path.exists(pathOut):
    os.mkdir(pathOut)

FTP_HOST = "nrt.cmems-du.eu"
FTP_USER = getpass("Username: ")
FTP_PASS = getpass("Password: ")

years = ["2016", "2017"]
months = [("0" + str(month))[-2:] for month in np.arange(1, 13)]

for year in years:
    for month in months:
        ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
        ftp.encoding = "utf-8"
        path = f"Core/SST_BS_SST_L3S_NRT_OBSERVATIONS_010_013/SST_BS_SST_L3S_NRT_OBSERVATIONS_010_013_b/{year}/{month}/"
        output_path = "CMEMS-black-sea-sst/"
        ftp.cwd(path)
        files = ftp.nlst()
        for file in tqdm(files, desc=f"Downloading {year}-{month}"):
            PATH = output_path + file
            with open(PATH, "wb") as fileToDownload:
                ftp.retrbinary(f"RETR {file}", fileToDownload.write)
        ftp.quit()
