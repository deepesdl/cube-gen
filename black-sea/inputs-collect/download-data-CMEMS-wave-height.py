import ftplib
import numpy as np
import os
from tqdm import tqdm
from getpass import getpass

pathOut = "CMEMS-black-sea-wave-height"

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
        path = f"Core/BLKSEA_MULTIYEAR_WAV_007_006/bs-hzg-wav-rean-h/{year}/{month}/"
        output_path = "CMEMS-black-sea-wave-height/"
        ftp.cwd(path)
        files = ftp.nlst()
        for file in tqdm(files, desc=f"Downloading {year}-{month}"):
            PATH = output_path + file
            with open(PATH, "wb") as fileToDownload:
                ftp.retrbinary(f"RETR {file}", fileToDownload.write)
        ftp.quit()
