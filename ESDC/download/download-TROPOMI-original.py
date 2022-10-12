import ftplib

FTP_HOST = "fluo.gps.caltech.edu"
FTP_USER = "anonymous"
FTP_PASS = ""

ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
ftp.encoding = "utf-8"

ftp.cwd("data/tropomi/gridded/SIF683")

filename = "TROPOMI-redSIF_global_05-2018--06-2021_daily_005deg.nc"
PATH = "/net/projects/deep_esdl/data/TROPOMI/data/" + filename
with open(PATH, "wb") as file:
    ftp.retrbinary(f"RETR {filename}", file.write)
    
ftp.quit()