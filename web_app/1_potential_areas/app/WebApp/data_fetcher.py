import pandas as pd
import numpy as np

class DataFetcher:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)

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
