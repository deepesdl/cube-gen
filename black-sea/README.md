# Ocean Black Sea Datacube Generation

Package dedicated to the generation of the Ocean Black Sea Datacube.

Source data:

- [Level 3 Chl-a, 300m, daily and monthly](http://www.eo4sibs.uliege.be/map/map.php?product=Ocean%20Colour%20(scale%20factor:%200.01)&is_netcdf=1)
- [Level 4, geostrophic currents, multi-mission gridded merged products for a period of 1 year, 0.0625°*0.0625°, daily](http://www.eo4sibs.uliege.be/map/map.php?product=Altimetry&is_netcdf=1) 
- [Black Sea Waves Reanalysis](https://resources.marine.copernicus.eu/product-detail/BLKSEA_MULTIYEAR_WAV_007_006/INFORMATION)
- [Black Sea - High Resolution and Ultra High Resolution L3S Sea Surface Temperature](https://resources.marine.copernicus.eu/product-detail/SST_BS_SST_L3S_NRT_OBSERVATIONS_010_013/INFORMATION)
- [Level 3 SSS, 0.25°*0.25°, 9-day averaged produced daily](http://www.eo4sibs.uliege.be/map/map.php?product=Sea%20Surface%20Salinity&is_netcdf=1)

Source data is available from EO4SIBS (3 datasets) and CMEMS (2 datasets). To download data (5 sources):

```
# Download Sea Surface Temperature
python inputs-collect/download-data-CMEMS-SST.py

# Download Significant Wave Height
python inputs-collect/download-data-CMEMS-wave-height.py

# Download Surface Currents
python inputs-collect/download-data-EO4SIBS-altimetry.py

# Download Chlorophyll
python inputs-collect/download-data-EO4SIBS-chl.py

# Download Sea Surface Salinity
python inputs-collect/download-data-EO4SIBS-SSS.py
```

To convert source data to zarr in the S3 deepESDL bucket:

```
nc2zarr -c inputs-preprocess/nc2zarr-CMEMS-black-sea-sst.yml
nc2zarr -c inputs-preprocess/nc2zarr-CMEMS-black-sea-wave-height.yml
nc2zarr -c inputs-preprocess/nc2zarr-EO4SIBS-black-sea-altimetry.yml
nc2zarr -c inputs-preprocess/nc2zarr-EO4SIBS-black-sea-chl.yml
nc2zarr -c inputs-preprocess/nc2zarr-EO4SIBS-black-sea-sss.yml
```

To preprocess, aggregate, resample, and generate the final data cube:

```
python output-merge/black-sea-datacube.py
```