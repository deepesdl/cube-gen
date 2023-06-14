from tqdm import tqdm
import os
import cdsapi
from multiprocessing import Pool, Manager

def download_data(args):
    pathOut, variable, year, month, progress_queue = args
    directory = os.path.join(pathOut, variable, year)
    
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass

    filename = f"{variable}.hh.*.era5.{month}.{year}.nc"
    filepath = os.path.join(directory, filename)

    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'year': year,
            'month': month,
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
            'variable': variable,
        },
        filepath
    )

    progress_queue.put(1)
    return f"Downloaded {filepath}"

def main():
    pathOut = "~/data/ERA5/source"
    pathOut = os.path.expanduser(pathOut)

    if not os.path.exists(pathOut):
        os.makedirs(pathOut)

    years = [str(year) for year in range(1971, 2022)]
    months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    variables = ['2m_temperature', 'evaporation', 'maximum_2m_temperature_since_previous_post_processing', 'minimum_2m_temperature_since_previous_post_processing', 'total_precipitation', 'surface_solar_radiation_downwards']

    args_list = []
    for variable in variables:
        for year in years:
            for month in months:
                args_list.append((pathOut, variable, year, month))

    with Pool() as pool, Manager() as manager:
        progress_queue = manager.Queue()
        total_tasks = len(args_list)
        results = []

        with tqdm(total=total_tasks) as pbar:
            for result in pool.imap_unordered(download_data, [(args + (progress_queue,)) for args in args_list]):
                results.append(result)
                pbar.update(progress_queue.get())

    for result in results:
        print(result)

if __name__ == '__main__':
    main()
