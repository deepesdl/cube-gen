# ESDC Configuration (Draft) (To be revised)

Package dedicated to the new ESDC configuraton. 

## Spatio-temporal grid specification

As a continuation of the previous ESDC, the new configuration will follow the same spatio-tempotal
grid (at two spatial resolutions). The included variables will be extended to the end of 2021,
subject to each variable availability.

- **Temporal resolution**: 8D
- **Spatial resolution**: 0.25 and 0.0833 degrees
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

### SIF Collection

#### GOME-2

*2 Variables*

Data source: [https://data.jrc.ec.europa.eu/dataset/21935ffc-b797-4bee-94da-8fec85b3f9e1](https://data.jrc.ec.europa.eu/dataset/21935ffc-b797-4bee-94da-8fec85b3f9e1)

Time period: 2007-2018

Temporal resolution: 8D

Spatial resolution: 0.05 degrees

- Downscaled SIF 740 nm JJ Method
- Downscaled SIF 740 nm PK Method

#### GOSIF

*1 Variable*

Data source: [https://globalecology.unh.edu/data/GOSIF.html](https://globalecology.unh.edu/data/GOSIF.html)

Time period: 2000-2021

Temporal resolution: 8D

Spatial resolution: 0.05 degrees

- SIF 757 nm

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

Temporal resolution: 1H

Spatial resolution: 0.25 degrees

- Air Temperature 2 m mean
- Air Temperature 2 m min
- Air Temperature 2 m max
- Total Precipitation
- Surface Shortwave Downwelling Radiation
- Potential Evaporation
- Evaporation

### MCD43C4 MODIS/Terra+Aqua BRDF/Albedo Nadir BRDF-Adjusted Reflectance Daily L3 Global 0.05 Deg CMG

*7 Variables*

Data source: [https://lpdaac.usgs.gov/products/mcd43c4v061/](https://lpdaac.usgs.gov/products/mcd43c4v061/)

Time period: 2000-2021

Temporal resolution: 1D

Spatial resolution: 0.05 degrees

- Nadir BRDF Adjusted Reflectance Blue
- Nadir BRDF Adjusted Reflectance Green
- Nadir BRDF Adjusted Reflectance Red
- Nadir BRDF Adjusted Reflectance NIR
- Nadir BRDF Adjusted Reflectance SWIR 1
- Nadir BRDF Adjusted Reflectance SWIR 2
- Nadir BRDF Adjusted Reflectance SWIR 3