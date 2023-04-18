# Polar Datacube Generation

Information dedicated to the generation of the Polar Datacube.

## Cube generation process

The cube generation process is divided in four phases:

> **Note**
>
> Before running the following scripts, you must activate the `cube-gen` conda environment by running `conda activate cube-gen`.

### 1. Downloading required raw datasets

> **Note**
>
> When downloading the datasets, a path `data/polar/source/` is created in the user home path. All datasets are downloaded into this folder for further preprocessing.

Datasets were downloaded via the source information provided in `cube.geojson`. Datasets were downloaded in different formats: `.nc`, `.tif`, `.shp`. Some datasets were compressed and this step includes the extraction of the data.

To download the datasets it is required to run the following file:

```
# Download all files
python inputs-collect/download-sources.py
```

### 2. Preprocessing datasets

The raw data is preprocessed in order to create a single input `.zarr` cube per dataset. The preprocessing steps might involve time resampling and/or spatial resampling according to the dataset. The preprocessing code for each dataset is found at the `inputs-preprocess` folder. Note that some datasets have multiple parts according to the preprocessing steps that were applied:

```
# Curie Depth Estimates
python inputs-preprocess/curie-depth.py # Convert files to zarr
python inputs-preprocess/curie-depth-resample.py # Spatial resampling

# Geothermal Heat Flow
python inputs-preprocess/geothermal-heat-flow.py # Convert files to zarr
python inputs-preprocess/geothermal-heat-flow-resample.py # Spatial resampling

# Geothermal Heat Flow Uncertainty
python inputs-preprocess/geothermal-heat-flow-uncertainty.py # Convert files to zarr
python inputs-preprocess/geothermal-heat-flow-uncertainty-resample.py # Spatial resampling

# Magnetic Anomaly
python inputs-preprocess/magnetic-anomaly.py # Convert files to zarr
python inputs-preprocess/magnetic-anomaly-resample.py # Spatial resampling

# Subglacial Lakes
python inputs-preprocess/subglacial-lakes-2013-2017.py # Convert files to zarr
python inputs-preprocess/subglacial-lakes-2013-2017-resample.py # Spatial resampling

# Ice Thickness
python inputs-preprocess/bedrock-ice-thickness.py # Convert files to zarr
python inputs-preprocess/bedrock-ice-thickness-resample.py # Spatial resampling
```

After preprocessing, all `.zarr` cubes were uploaded to `s3://deep-esdl-input/` by running the following file:

```
# Upload all datasets
python inputs-preprocess/upload-to-s3.py
```

> **Note**
>
> Users not belonging to the DeepESDL cube-gen team must provide a different bucket. This can be changed inside the `inputs-preprocess/upload-to-s3.py` file.

### 3. Merging all datasets into a single cube

All `.zarr` cubes are loaded and merged by their coordinates into a single `.zarr` cube.

```
# Merge all datasets
python output-merge/merge.py
```

### 4. Postprocessing

A patch of metadata is added to the final cube using `xcube patch` and `output-postprocess/patch.yaml` by running:

```
# Merge all datasets
output-postprocess/patch-cube.sh
```