import requests


def download_dataset_by_date(dataset, start_date, end_date, output_filename):

    url_base = "http://www.eo4sibs.uliege.be/map/netcdf_export"

    url_templ_1 = (
        url_base + "/netcdf_export.php"
        "?start_time={start_time}"
        "&end_time={end_time}"
        "&dataset={dataset}"
    )

    url_templ_2 = url_base + "/{filename}"

    response = requests.get(
        url_templ_1.format(start_time=start_date, end_time=end_date, dataset=dataset)
    )
    if not response.ok:
        response.raise_for_status()

    filename = response.text
    response = requests.get(url_templ_2.format(filename=filename), stream=True)
    if not response.ok:
        response.raise_for_status()

    with open(output_filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=16 * 1024):
            if chunk:
                f.write(chunk)
