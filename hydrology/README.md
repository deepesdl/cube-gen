# Hydrology Datacubes Generation

Information dedicated to the generation of the Hydrology Datacubes. By using the following recipe, 28 hydrology data cubes can be reproduced (One cube per region)

The total storage required for the generation of these cube is 490 GB.

## Cubes generation process

The cubes generation process is divided in four phases:

### 1. Downloading required raw datasets

Datasets were downloaded from the `4dmed_data.eodchosting.eu` sftp host. The following folders were downloaded recursively using the sftp protocol:

> **Note**
>
> Users must provide their own credentials to access the sftp host.

- `/4dmed_data/CNR_products/precipitation_GPM_CPC_SM2RAIN-ASCAT`
- `/4dmed_data/TUWien_RT1_SM`
- `/4dmed_data/GLEAM_openloop_V1.1`
- `/4dmed_data/SWE/SWE_CPC_GPM_ERA5downT_RadGhent_filter5mm`

Datasets were downloaded into a folder named `data/hydrology/source` in the user home path.

> **Note**
>
> The path `data/hydrology/source` should be created by the user and the folders from the host should be downloaded here.

The Snow Water Equivalent (SWE) product is zipped and has to be unzipped by running the following command:

```
python inputs-collect/extract-gz-SWE.py # Extract nc files
```

### 2. Preprocessing datasets

The raw data is preprocessed in order to create a single input `.zarr` cube per dataset and region. The preprocessing steps might involve time resampling and/or spatial resampling according to the dataset. The preprocessing code for each dataset is found at the `inputs-preprocess` folder. Note that some datasets have multiple parts according to the preprocessing steps that were applied:

**If you wish to execute the below scripts please ensure to adjust the `root` parameter in the scripts to point to a s3 bucket which you have read-write access to.**

```
# Evaporation
python inputs-preprocess/evaporation-to-zarr.py # Convert files to zarr
python inputs-preprocess/evaporation-to-s3.py # Upload full cube to the s3 bucket

# Precipitation
python inputs-preprocess/precipitation-to-zarr.py # Convert files to zarr
python inputs-preprocess/precipitation-to-s3.py # Upload full cube to the s3 bucket

# Soil Moisture
python inputs-preprocess/sm-to-zarr.py # Convert files to zarr
python inputs-preprocess/sm-to-s3.py # Upload full cube to the s3 bucket

# Snow Water Equivalent
python inputs-preprocess/swe-to-zarr.py # Convert files to zarr
python inputs-preprocess/swe-to-s3.py # Upload full cube to the s3 bucket
```

### 3. Merging all datasets into a single cube

The `.zarr` cubes are loaded per region, aggregated to a daily temporal 
resolution and merged by their coordinates and timesteps into a single `.zarr` cube.

**If you wish to execute the below scripts please ensure to adjust the `root` parameter in the scripts to point to a s3 bucket which you have read-write access to.**

```
# Merge all datasets
python output-merge/daily_aggregates_and_merge.py
```

### 4. Postprocessing

A patch of metadata is added to the final cubes using `xcube patch` by running:

```
# Patch all cubes
output-postprocess/patch.sh
```

If you wish to merge all subcubes into one, please execute the following:

```
# Merge all subcubes into a single cube
python output-postprocess/merge-all-regions-into-one-cube.py
```

Update metadata of the final cube, containing all subregions:

```
# Update metadata of final cube:
xcube patch s3://deep-esdl-output/hydrology-1D-0.009deg-1x1102x966-1.0.0.levels --metadata patch-hydrology-1D-0.009deg-1x1102x2415.yaml -v
```
**If you wish to execute the above script please ensure to adjust the s3 bucket path to point to the bucket which you have read-write access to.**