import pandas as pd
import numpy as np
import pickle
import streamlit as st

LOOKER_URL = "https://lookerstudio.google.com/embed/reporting/eaab71cb-575f-4f7c-b9ac-97942e43d017/page/r2W2D"

class DataFetcher:
    def __init__(self, parquet_path):
        self.data = pd.read_parquet(parquet_path)

    def fetch_data(self, latitude, longitude):
        # Calculate the distance between the given lat/lon and the dataset lat/lon
        self.data['distance'] = np.sqrt((self.data['latitude'] - latitude)**2 + (self.data['longitude'] - longitude)**2)
        # Find the row with the minimum distance
        row = self.data.loc[self.data['distance'].idxmin()]

        # Check if the distance is within an acceptable tolerance (e.g., 0.01 degrees)
        tolerance = 0.02
        if row['distance'] > tolerance:
            return None
        return row.to_dict()


# Load the models 
def load_model(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

# Read parquet file
@st.cache_data
def read_parquet(filename):
    df = pd.read_parquet(
        filename,
        engine="pyarrow",
        dtype_backend="pyarrow",
    )
    return df