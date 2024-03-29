# Ocean Datacube Generation

Information dedicated to the generation of the Ocean Datacubes. By using the following recipe two ocean data cubes can be reproduced:

1) The Particulate Organic Carbon (POC) Data Cube at 4 km and   
2) the Oceanic Export Production, Phytoplankton Carbon and Primary Production Data Cube at 9 km.

The total storage required for the generation of these cube is 490 GB.

## Cubes generation process

The cubes generation process is divided in four phases:

### 1. Downloading required raw datasets

Datasets were downloaded into a folder named `data` in the user home path via the source information provided in `cube4km.geojson` and `cube9km.geojson`. Datasets were downloaded in `.nc` format.

To download the datasets, it is required to run the following files under the `cube-gen` python environment:
```
conda activate cube-gen
```

The files can be executed using the following commands:

```
# Download all files
cd inputs-collect/
python download-sources-4km.py
python download-sources-9km.py

# Download additional files for 9km cube
python download-sources-add-9km-DOC.py
python download-sources-add-9km-Phytoplankton.py
python download-sources-add-9km.py
```

### 2. Preprocessing datasets

The raw data is preprocessed in order to create a single input `.zarr` cube per dataset. The preprocessing steps might involve time resampling and/or spatial resampling according to the dataset. The preprocessing code for each dataset is found at the `inputs-preprocess` folder. Note that some datasets have multiple parts according to the preprocessing steps that were applied:

**If you wish to execute the below scripts please ensure to adjust the `root` parameter in the scripts to point to a s3 bucket which you have read-write access to.**

```
# Oceanic Export Production
cd ..
python inputs-preprocess/oceanic-export-production-to-zarr.py # Convert files to zarr
python inputs-preprocess/oceanic-export-production-to-s3.py # Upload full cube to the s3 bucket

# Particulate Organic Carbon
python inputs-preprocess/particulate-organic-carbon-to-zarr.py # Convert files to zarr

# Phytoplankton Carbon
python inputs-preprocess/phytoplankton-carbon-to-zarr.py # Convert files to zarr
python inputs-preprocess/phytoplankton-carbon-to-s3.py # Upload full cube to the s3 bucket

# Primary Production
python inputs-preprocess/primary-production-to-zarr.py # Convert files to zarr
python inputs-preprocess/primary-production-to-s3.py # Upload full cube to the s3 bucket
```

### 3. Merging all datasets into a single cube

All `.zarr` cubes are loaded and merged by their coordinates and timesteps into a single `.zarr` cube.

**If you wish to execute the below scripts please ensure to adjust the `root` parameter in the scripts to point to a s3 bucket which you have read-write access to.**

```
# Merge all datasets
python output-merge/merge-4km.py
python output-merge/merge-9km.py
```

### 4. Postprocessing

A patch of metadata is added to the final cubes using `xcube patch` and `output-postprocess/patch-4km.yaml`/`output-postprocess/patch-9km.yaml` by running:

```
# Merge all datasets
output-postprocess/patch.sh
```

**If you wish to execute the above script please ensure to adjust the s3 bucket path to point to the bucket which you have read-write access to.**