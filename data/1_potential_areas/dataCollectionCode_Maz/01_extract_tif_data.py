# # -*- coding: utf-8 -*-
# """
# Created on Sun May 12 23:14:45 2024
# @author: mazhar
# """

import os
from datetime import datetime

import numpy as np
import pandas as pd
import rasterio
from pyproj import CRS, Transformer
from tqdm import tqdm

print("#" * 120)

zone = "zone9"

# Directory to save CSV files
save_dir_csv = "./csv_files/test_csv/zone9"
os.makedirs(save_dir_csv, exist_ok=True)
print(f"Directory: {save_dir_csv}, checked and created if not existing.")

# Directory containing TIFF files
tif_dir = "./images/test_images/zone9"
tif_file_paths = [
    os.path.join(tif_dir, f) for f in os.listdir(tif_dir) if f.endswith(".tif")
]
print(f"Files in tif directory: {tif_file_paths}")
print(f"Number of files in tif directory: {len(tif_file_paths)}")


def extract_data(tif_path):
    with rasterio.open(tif_path) as dataset:
        # zone = tif_path.split("/")[-2]  # Extracting zone from the path
        metadata = dataset.meta
        crs = dataset.crs
        bounds = dataset.bounds
        width = dataset.width
        height = dataset.height
        count = dataset.count  # Number of bands
        dtypes = dataset.dtypes
        indexes = dataset.indexes
        driver = dataset.driver
        transform = dataset.transform
        band_names = dataset.descriptions or [
            f"Band {i+1}" for i in range(dataset.count)
        ]
        data = [dataset.read(i + 1) for i in range(dataset.count)]
        rows, cols = data[0].shape
        latitudes, longitudes, values = [], [], {band: [] for band in band_names}
        transformer = (
            Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
            if crs.to_epsg() != 4326
            else None
        )

        for row in range(rows):
            for col in range(cols):
                x, y = transform * (col, row)
                lon, lat = transformer.transform(x, y) if transformer else (x, y)
                latitudes.append(lat)
                longitudes.append(lon)
                for i, band in enumerate(band_names):
                    values[band].append(data[i][row, col])

        return {
            "metadata": metadata,
            "crs": crs,
            "bounds": bounds,
            "transform": transform,
            "width": width,
            "height": height,
            "count": count,
            "dtypes": dtypes,
            "indexes": indexes,
            "driver": driver,
            "latitudes": latitudes,
            "longitudes": longitudes,
            "values": values,
            "band_names": band_names,
            "zone": zone,
        }


def data_to_dataframe(data):
    df = pd.DataFrame(
        {
            "Latitude": data["latitudes"],
            "Longitude": data["longitudes"],
            "Zone": [data["zone"]]
            * len(data["latitudes"]),  # Repeating the zone value for each row
        }
    )
    for band in data["band_names"]:
        df[band] = data["values"][band]
    return df


def save_to_csv(df, csv_dir, tif_path):
    csv_file_name = os.path.basename(tif_path).replace(".tif", ".csv")
    csv_full_path = os.path.join(csv_dir, csv_file_name)
    df.to_csv(csv_full_path, index=False)
    return csv_full_path


for tif_path in tqdm(
    tif_file_paths, colour="green", desc="Extracting Data from TIFF Files"
):
    data = extract_data(tif_path)

    # Print metadata
    # print("Metadata:", data["metadata"])
    # print("CRS:", data["crs"])
    # print("Bounds:", data["bounds"])
    # print("Transform:", data["transform"])
    # print("Width:", data["width"])
    # print("Height:", data["height"])
    # print("Count:", data["count"])
    # print("Data Types:", data["dtypes"])
    # print("Indexes:", data["indexes"])
    # print("Driver:", data["driver"])

    # # Print the number of latitude, longitude, and data values
    # print(f"Number of latitude values: {len(data['latitudes'])}")
    # print(f"Number of longitude values: {len(data['longitudes'])}")
    # print(
    #     f"Number of data values in each band: {len(data['values'][data['band_names'][0]])}"
    # )
    # # Print all latitudes, longitudes, and data values for each band
    # print("All Latitudes, Longitudes, and Values for each band:")
    # for i in range(len(data["latitudes"])):
    #     print(f"Latitude: {data['latitudes'][i]}, Longitude: {data['longitudes'][i]}")
    #     for band in data["band_names"]:
    #         print(f"  {band} Value: {data['values'][band][i]}")

    df = data_to_dataframe(data)
    csv_file_path = save_to_csv(df, save_dir_csv, tif_path)

print(f"Data extraction completed, CSV files saved to: {save_dir_csv}")
print(f"Number of CSV files saved: {len(os.listdir(save_dir_csv))}")

print("#" * 120)
