# ESDC Configuration (Draft) (To be revised)

Package dedicated to the new ESDC configuraton.

## Spatio-temporal grid specification

- **Temporal resolution**: 1D
- **Spatial resolution**: 0.0833 degrees
- **Extended time period to**: 2021-12-31

## Variables specification

### Global Land Evaporation Amsterdam Model (GLEAM)

*10 Variables*

Data source: [https://www.gleam.eu/](https://www.gleam.eu/)
Time period: 1980-2021
Temporal resolution: 1D
Spatial resolution: 0.25 degrees

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
Time period: 2000-2021
Temporal resolution: 8D
Spatial resolution: 0.0833 degrees

- Gross Primary Production
- Latent Energy
- Net Ecosystem Exchange
- Net Radiation
- Sensible Heat
- Terrestrial Ecosystem Respiration

### SIF Collections

#### GOME-2

*2 Variables*

Data source: [https://data.jrc.ec.europa.eu/dataset/21935ffc-b797-4bee-94da-8fec85b3f9e1](https://data.jrc.ec.europa.eu/dataset/21935ffc-b797-4bee-94da-8fec85b3f9e1)
Time period: 2007-2018
Temporal resolution: 8D
Spatial resolution: 0.05 degrees

- Downscaled SIF 740 nm JJ Method
- Downscaled SIF 740 nm PK Method

#### GOSIF

*2 Variables*

Data source: [https://globalecology.unh.edu/data/GOSIF.html](https://globalecology.unh.edu/data/GOSIF.html)
Time period: 2000-2021
Temporal resolution: 8D
Spatial resolution: 0.05 degrees

- SIF 757 nm
- SIF Derived GPP

#### TROPOMI

*1 Variable*

Data source: [https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2018GL079031](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2018GL079031)
Time period: 2018-2021
Temporal resolution: 8D
Spatial resolution: 0.0833 degrees

- SIF 740 nm

#### Reconstructed TROPOMI (RTSIF)

*1 Variable*

Data source: [https://www.nature.com/articles/s41597-022-01520-1](https://www.nature.com/articles/s41597-022-01520-1)
Time period: 2000-2021
Temporal resolution: 8D
Spatial resolution: 0.05 degrees

- Reconstructed SIF

### ERA5

*7 Variables*

Data source: [https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels)
Time period: 1950-2021
Temporal resolution: 1D
Spatial resolution: 0.25 degrees

- Air Temperature 2 m mean
- Air Temperature 2 m min
- Air Temperature 2 m max
- Total Precipitation
- Surface Shortwave Downwelling Radiation
- Potential Evaporation
- Evaporation

### ESA CCI

*8 Variables*

Data source: [https://climate.esa.int/en/odp/#/dashboard](https://climate.esa.int/en/odp/#/dashboard)

- Soil Moisture Combined: 1978-2020, 1D, 0.25
- Multisensor LST Day: 1995-2020, 1D, 0.01
- Multisensor LST Night: 1995-2020, 1D, 0.01
- Total Column Water Vapour: 2002-2017, 1D, 0.05
- Sea Surface Temperature: 1981-2016, 1D, 0.05
- Sea Surface Salinity: 2010-2020, 1D, 0.25
- Sea Ice Concentration: 2002-2017, 1D, 0.25
- Oceacn Chl-a: 1997-2020, 1D, 0.04

### MODIS MCD43A4 Nadir BRDF Adjusted Reflectance

*9 Variables*

Data source: [https://lpdaac.usgs.gov/products/mcd43a4v006/](https://lpdaac.usgs.gov/products/mcd43a4v006/)
Time period: 2000-2021
Temporal resolution: 1D
Spatial resolution: 0.005 degrees

- Nadir BRDF Adjusted Reflectance Blue
- Nadir BRDF Adjusted Reflectance Green
- Nadir BRDF Adjusted Reflectance Red
- Nadir BRDF Adjusted Reflectance NIR
- Nadir BRDF Adjusted Reflectance SWIR 1
- Nadir BRDF Adjusted Reflectance SWIR 2