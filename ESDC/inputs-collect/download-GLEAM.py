import os
import paramiko
from tqdm import tqdm
from multiprocessing import Pool

def download_file(args):
    host, port, username, password, remote_file, local_file = args
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    sftp.get(remote_file, local_file)

    sftp.close()
    transport.close()

def download_files(host, port, username, password, remote_dir, local_dir):
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    remote_years = sftp.listdir(remote_dir)

    tasks = []
    
    for year in range(1980, 2023):
        str_year = str(year)
        if str_year in remote_years:
            remote_year_dir = os.path.join(remote_dir, str_year)
            local_year_dir = os.path.join(local_dir, str_year)

            if not os.path.exists(local_year_dir):
                os.makedirs(local_year_dir)

            remote_files = sftp.listdir(remote_year_dir)

            for file in remote_files:
                remote_file = os.path.join(remote_year_dir, file)
                local_file = os.path.join(local_year_dir, file)

                tasks.append((host, port, username, password, remote_file, local_file))

    sftp.close()
    transport.close()

    # Server Restriction for 8 simultaneously downloads (?)
    with Pool(8) as pool:
        with tqdm(total=len(tasks), desc="Downloading files") as pbar:
            for _ in pool.imap_unordered(download_file, tasks):
                pbar.update(1)

def main():
    print("Please enter the credentials you got per mail from GLEAM")
    host = input("Enter the host (without 'sftp://'): ")
    port = int(input("Enter the port: "))
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    remote_dir = "./data/v3.7a/daily"
    local_dir = "~/data/GLEAM/source"

    local_dir = os.path.expanduser(local_dir)

    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    download_files(host, port, username, password, remote_dir, local_dir)

if __name__ == '__main__':
    main()
