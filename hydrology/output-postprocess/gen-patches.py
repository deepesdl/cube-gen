from xcube.core.store import find_data_store_extensions
from xcube.core.store import get_data_store_params_schema
from xcube.core.store import new_data_store

import yaml

store_output = new_data_store("s3", root="deep-esdl-output")
datasets = list(store_output.get_data_ids())

hydro_datasets = [s for s in datasets if "hydrology" in s]

xcube_patches = []

for cube_id in hydro_datasets:

    to_dump = {
        "zarr_consolidated_format": 1,
        "metadata": {
            ".zattrs": {
                "Conventions": "CF-1.10",
                "acknowledgment": "All data providers are acknowledged inside each variable",
                "contributor_name": ["University of Leipzig", "Brockmann Consult GmbH"],
                "contributor_url": ["https://www.uni-leipzig.de/", "https://www.brockmann-consult.de/"],
                "creator_name": ["University of Leipzig", "Brockmann Consult GmbH"],
                "creator_url": ["https://www.uni-leipzig.de/", "https://www.brockmann-consult.de/"],
                "publisher_name": "DeepESDL Team",
                "publisher_url": "https://www.earthsystemdatalab.net/",
                "id": cube_id,
                "project": "DeepESDL",
                "title": "BICEP Pools and Fluxes of the Ocean Biological Carbon Pump",
                "license": "Terms and conditions of the DeepESDL data distribution",
            },
            "time/.zattrs": {
                "long_name": 'time',
                "standard_name": 'time',
            },
            "lat/.zattrs": {
                "long_name": 'latitude',
                "standard_name": 'latitude',
                "units": "degrees_north"
            },
            "lon/.zattrs": {
                "long_name": 'longitude',
                "standard_name": 'longitude',
                "units": "degrees_east"
            },
            "E/.zattrs": {
                "long_name": 'Evaporation',
                "standard_name": 'evaporation',
                "description": 'Evaporation',
                "units": "mm d^-1",
                "processing_steps": ['Gridding nc datasets'],
                "acknowledgement": "Hydrology 4D",
                "original_name": "E",
                "original_scale_factor": 1.0,
                "original_add_offset": 0.0,
                "source": '4dmed_data.eodchosting.eu/4dmed_data/GLEAM_openloop_V1.1',
            },
            "precip/.zattrs": {
                "long_name": 'Precipitation',
                "standard_name": 'precipitation',
                "description": 'Precipitation',
                "units": "mm d^-1",
                "processing_steps": ['Gridding nc datasets'],
                "acknowledgement": "Hydrology 4D",
                "original_name": "precip",
                "original_scale_factor": 1.0,
                "original_add_offset": 0.0,
                "source": '4dmed_data.eodchosting.eu/4dmed_data/precipitation_GPM_CPC_SM2A',
            },
            "SM/.zattrs": {
                "long_name": 'Soil Moisture',
                "standard_name": 'soil_moisture',
                "description": 'Soil Moisture',
                "units": "% Relative Saturation",
                "processing_steps": ['Gridding nc datasets'],
                "acknowledgement": "Hydrology 4D",
                "original_name": "SM",
                "original_scale_factor": 1.0,
                "original_add_offset": 0.0,
                "source": '4dmed_data.eodchosting.eu/4dmed_data/TUWien_RT1_SM',
            },
            "SWE/.zattrs": {
                "long_name": 'Snow Water Equivalent',
                "standard_name": 'snow_water_equivalent',
                "description": 'Snow Water Equivalent',
                "units": 1,
                "processing_steps": ['Gridding nc datasets'],
                "acknowledgement": "Hydrology 4D",
                "original_name": "SWE",
                "original_scale_factor": 1.0,
                "original_add_offset": 0.0,
                "source": '4dmed_data.eodchosting.eu/4dmed_data/SWE/SWE_CPC_GPM_ERA5downT_RadGhent_filter5mm',
            },
        }
    }

    site = cube_id.split("-")[1]

    with open(f'patch-{site}.yaml', 'w') as file:
        yaml.dump(to_dump, file)
        
    xcube_patches.append(f"xcube patch s3://deep-esdl-output/{cube_id} --metadata patch-{site}.yaml -v")
    
with open('patch.sh', 'w') as file:
    file.writelines(item + '\n' for item in xcube_patches)