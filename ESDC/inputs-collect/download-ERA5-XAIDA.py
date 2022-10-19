import cdsapi
import numpy as np
import os

years = np.arange(1959,2022)
months = [("0" + str(x))[-2:] for x in np.arange(1,13)]

c = cdsapi.Client()

for year in years:
    for month in months:
    
        pathFilename = f'/net/projects/deep_esdl/data/ERA5/ERA5-{year}-{month}-XAIDA.nc'
        
        if not os.path.exists(pathFilename):
    
            print(f"Downloading {year}-{month}...")

            c.retrieve(
                'reanalysis-era5-single-levels',
                {
                    'product_type': 'reanalysis',
                    'format': 'netcdf',
                    'variable': [
                        '10m_u_component_of_wind', '10m_v_component_of_wind', '10m_wind_gust_since_previous_post_processing',
                        '2m_dewpoint_temperature', 'mean_sea_level_pressure', 'runoff',
                        'skin_temperature', 'surface_pressure', 'total_cloud_cover',
                    ],
                    'year': f'{year}',
                    'month': f'{month}',
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
                },
                pathFilename)
            
        else:
            
            print(pathFilename + " already exists!")