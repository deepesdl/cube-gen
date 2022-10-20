# Earth System Data Cube (ESDC) v3.0.0

Package dedicated to the ESDC v3.0.0 configuraton. 

## Table of Contents
- [Spatio-temporal grid specification](#spatio-temporal-grid-specification)
- [Variables specification](#variables-specification)
- [Cube generation process](#cube-generation-process)

## Spatio-temporal grid specification

As a continuation of the previous ESDC, the new configuration wfollows the same spatio-tempotal
grid (at two spatial resolutions). The included variables will be extended to the end of 2021,
subject to each variable availability.

- **Time period**: 8D
- **Spatial resolution**: 0.25 and 0.0833 degrees
- **Extended time period to**: 2021-12-31

## Variables specification

Variables are specified according to their original specifications. This configuration
will be preprocessed to match the spatio-temporal grid specification for the extension
of the new ESDC.

### Global Land Evaporation Amsterdam Model (GLEAM)

*10 Variables*

Data source: [https://www.gleam.eu/](https://www.gleam.eu/)

- Actual Evaporation (E)
- Soil Evaporation (Eb)
- Interception Loss (Ei)
- Potential Evaporation (Ep)
- Snow Sublimation (Es)
- Transpiration (Et)
- Open-Water Evaporation (Ew)
- Evaporative Stress (S)
- Root-Zone Soil Moisture (SMroot)
- Surface Soil Moisture (SMsurf)

### Fluxcom

*6 Variables*

Data source: [https://www.fluxcom.org/](https://www.fluxcom.org/)

- Gross Primary Production
- Latent Energy
- Net Ecosystem Exchange
- Net Radiation
- Sensible Heat
- Terrestrial Ecosystem Respiration

### SIF Collection

#### GOME-2

*2 Variables*

Data source: [https://data.jrc.ec.europa.eu/dataset/21935ffc-b797-4bee-94da-8fec85b3f9e1](https://data.jrc.ec.europa.eu/dataset/21935ffc-b797-4bee-94da-8fec85b3f9e1)

- Downscaled SIF 740 nm JJ Method
- Downscaled SIF 740 nm PK Method

#### GOSIF

*1 Variable*

Data source: [https://globalecology.unh.edu/data/GOSIF.html](https://globalecology.unh.edu/data/GOSIF.html)

- SIF 757 nm

#### Reconstructed TROPOMI (RTSIF)

*1 Variable*

Data source: [https://www.nature.com/articles/s41597-022-01520-1](https://www.nature.com/articles/s41597-022-01520-1)

- Reconstructed SIF

### ERA5

*6 Variables*

Data source: [https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels)

- Air Temperature 2 m mean
- Air Temperature 2 m min
- Air Temperature 2 m max
- Total Precipitation
- Surface Shortwave Downwelling Radiation
- Evaporation

### MCD43C4 MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Reflectance Daily L3 Global 0.05 Deg CMG

*9 Variables*

Data source: [https://lpdaac.usgs.gov/products/mcd43c4v061/](https://lpdaac.usgs.gov/products/mcd43c4v061/)

- Nadir BRDF Adjusted Reflectance Blue
- Nadir BRDF Adjusted Reflectance Green
- Nadir BRDF Adjusted Reflectance Red
- Nadir BRDF Adjusted Reflectance NIR
- Nadir BRDF Adjusted Reflectance SWIR 1
- Nadir BRDF Adjusted Reflectance SWIR 2
- Nadir BRDF Adjusted Reflectance SWIR 3

Additional variables:

- NDVI (Produced from NBAR bands)
- NIRv (Produced from NBAR bands)
- kNDVI (Produced from NBAR bands)

#### ESA CCI Aerosol

*1 Variable*

Data source: [https://climate.esa.int/en/odp/#/project/aerosol](https://climate.esa.int/en/odp/#/project/aerosol)

- Aerosol Optical Thickness at 550 nm

#### ESA CCI Cloud

*3 Variables*

Data source: [https://climate.esa.int/en/odp/#/project/cloud](https://climate.esa.int/en/odp/#/project/cloud)

- Cloud Top Height 
- Cloud Optical Thickness 
- Cloud Top Temperature

#### ESA CCI Soil Moisture

*1 Variable*

Data source: [https://climate.esa.int/en/odp/#/project/soil-moisture](https://climate.esa.int/en/odp/#/project/soil-moisture)

- Volumetric Soil Moisture

#### Global Fire Emissions Database (GFED4)

*1 Variable*

Data source: [https://www.globalfiredata.org/](https://www.globalfiredata.org/)

- Burnt Area

## Cube generation process

The cube generation process is divided in four phases:

### 1. Downloading required raw datasets

These datasets are the input data. Each dataset can be a set of `.nc`, `.hdf`, or `.tif` files. These files contains data with its original configuration. The downloading code for each dataset is found at the `inputs-collect` folder. Note that some datasets can be acquired via `xcube-cci` and don't require to be downloaded. Additional datasets where acquired va ftp (e.g. GLEAM) or sftp (e.g. GFED4) and don't have a download program.

```
# MODIS: Download daily .hdf files
inputs-collect/download-MCD43C4.py

# GOME-2: Download 8-days .nc files
inputs-collect/download-GOME2-SIF.py

# GOSIF: Download 8-days and extract .tif files
inputs-collect/download-GOSIF.py
inputs-collect/extract-gz-gosif.py

# CCI-SM: Download daily .nc files
inputs-collect/download-cci-sm.py
```

### 2. Preprocessing datasets

The raw data is preprocessed in order to create a single input `.zarr` cube per dataset. The preprocessing steps might involve time resampling and/or spatial resampling according to the dataset.The preprocessing code for each dataset is found at the `inputs-preprocess` folder. Note that some datasets have multiple parts according to the preprocessing steps that were applied. By taking MODIS again as an example, it is required to run the following files for its preprocessing:

```
# GLEAM: Preprocessing
inputs-preprocess/gleam-data-cube.py # Concatenate .nc files
inputs-preprocess/gleam-data-cube-8d.py # Resample by 8-days
inputs-preprocess/gleam-metadata.py # Add initial metadata

# FLUXCOM: Preprocessing
inputs-preprocess/fluxcom-data-cube.py # Concatenate .nc files
inputs-preprocess/fluxcom-data-cube-8d-0.25deg.py # Resample to 0.25 degress
inputs-preprocess/fluxcom-metadata.py # Add initial metadata

# GOSIF: Preprocessing
inputs-preprocess/sif-gosif-data-cube-part1.py # Convert .tif to .zarr
inputs-preprocess/sif-gosif-data-cube-part2.py # Concatenate .zarr files
inputs-preprocess/sif-gosif-data-cube-0.25deg.py # Resample to 0.25 degrees
inputs-preprocess/sif-gosif-metadata.py # Add initial metadata

# GOME-2 JJ Method: Preprocessing
inputs-preprocess/sif-gome2-JJ-data-cube.py # Concatenate .nc files
inputs-preprocess/sif-gome2-JJ-data-cube-0.25deg.py # Resample to 0.25 degrees
inputs-preprocess/sif-gome2-JJ-metadata.py # Add initial metadata

# GOME-2 PK Method: Preprocessing
inputs-preprocess/sif-gome2-PK-data-cube.py # Concatenate .nc files
inputs-preprocess/sif-gome2-PK-data-cube-0.25deg.py # Resample to 0.25 degrees
inputs-preprocess/sif-gome2-PK-metadata.py # Add initial metadata

# RTSIF: Preprocessing
inputs-preprocess/sif-rtsif-data-cube-0.25deg.py # Resample to 0.25 degrees
inputs-preprocess/sif-rtsif-metadata.py # Add initial metadata

# ERA5: Preprocessing
inputs-preprocess/era5-data-cube-8d-part1.py # Resample by 1-day
inputs-preprocess/era5-data-cube-8d-part2.py # Resample by 8-days
inputs-preprocess/era5-data-cube-8d-0.25deg.py # Resample to 0.25 degrees
inputs-preprocess/era5-metadata.py # Add initial metadata

# MODIS: Preprocessing
inputs-preprocess/modis-mcd43c4-data-cube-part1.py # Convert .hdf to .zarr
inputs-preprocess/modis-mcd43c4-data-cube-part2.py # Concatenate .zarr files
inputs-preprocess/modis-mcd43c4-data-cube-part3.py # Compute spectral indices
inputs-preprocess/modis-mcd43c4-data-cube-part4.py # Merge spectral indices and bands
inputs-preprocess/modis-mcd43c4-data-cube-8d.py # Resample by 8-days
inputs-preprocess/modis-mcd43c4-data-cube-8d-0.25deg.py # Resample to 0.25 degrees
inputs-preprocess/modis-mcd43c4-data-cube-8d-0.25deg-mask.py # Mask out water pixels
inputs-preprocess/modis-metadata.py # Add initial metadata

# CCI Aerosol: Preprocessing
inputs-preprocess/cci-aod550-8d-0.25deg.py # Resample to 0.25 degrees
inputs-preprocess/cci-aod550-metadata.py # Add initial metadata

# CCI Cloud: Preprocessing
inputs-preprocess/cci-cloud-8d-0.25deg.py # Resample to 0.25 degrees
inputs-preprocess/cci-cloud-metadata.py # Add initial metadata

# CCI Soil Moisture: Preprocessing
inputs-preprocess/cci-sm-8d-0.25deg.py # Resample to 0.25 degrees
inputs-preprocess/cci-sm-metadata.py # Add initial metadata

# GFED4: Preprocessing
inputs-preprocess/gfed4-burntarea-data-cube-8d-0.25deg.py # Resample to 0.25 degrees
inputs-preprocess/gfed4-burntarea-metadata.py # Add initial metadata
```

### 3. Merging all datasets into a single cube

All `.zarr` cubes are loaded and merged by their coordinates into a single `.zarr` cube.

```
# Merge all datasets
output-merge/esdc-data-cube-8d-0.25deg.py
```

### 4. Postprocessing

A patch of metadata is added to the final cube using `xcube patch` and `output-postprocess/patch.yaml`.