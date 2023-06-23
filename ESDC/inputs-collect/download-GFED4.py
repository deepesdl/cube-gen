import requests
from tqdm import tqdm
import os

path_out = "~/data/GFED4/source"
path_out = os.path.expanduser(path_out)

if not os.path.exists(path_out):
    os.makedirs(path_out)

base_url = 'https://daac.ornl.gov/daacdata/global_vegetation/fire_emissions_v4_R1/data/Monthly/'
file_prefix = 'GFED4.0_MQ_'

years = range(1995, 2017)
months = ['{:02d}'.format(m) for m in range(1, 13)]

session = requests.Session()
auth_url = 'https://urs.earthdata.nasa.gov/oauth/authorize?app_type=401&client_id=QyeRbBJg8YuY_WBh-KBztA&response_type=code&redirect_uri=https%3A%2F%2Fdaac.ornl.gov%2Fdaacdata%2Fdoesntmater&state=aHR0cHM6Ly9kYWFjLm9ybmwuZ292L2RhYWNkYXRhL2dsb2JhbF92ZWdldGF0aW9uL2ZpcmVfZW1pc3Npb25zX3Y0X1IxL2RhdGEvTW9udGhseS8'

username = input("Enter your username: ")
password = input("Enter your password: ")

auth_response = session.get(auth_url, auth=(username, password))
session.auth = (username, password)

if auth_response.status_code != 200:
    print('Authentication failed:', auth_response.status_code)
    exit()


def handle_data_url_response(response, month, year):
    if response.status_code != 200:
        if response.status_code == 404:
            print(f'Data not available for {month}/{year}')
        else:
            print('Failed to access the data URL:', response.status_code)


def handle_file_url_response(response, file_url):
    if response.status_code != 200:
        if response.status_code == 404:
            print("---")
        else:
            print(f'Failed to download: {file_url}')


for year in years:
    for month in months:
        file_name = file_prefix + str(year) + month + '_BA.hdf'
        data_url = base_url + file_name

        response = session.get(data_url, auth=(username, password), allow_redirects=False)
        print(response.status_code)

        handle_data_url_response(response, month, year)

        file_url = base_url + file_name
        response = session.get(file_url, auth=(username, password), allow_redirects=False, stream=True)

        handle_file_url_response(response, file_url)

        if response.status_code != 200:
            continue

        file_path = os.path.join(path_out, file_name)
        total_size = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc=file_name)

        with open(file_path, 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                progress_bar.update(len(data))

        progress_bar.close()
        print(f'Downloaded: {file_name}')
        print("---")
