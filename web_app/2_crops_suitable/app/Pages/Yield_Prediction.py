import streamlit as st
import pandas as pd
import numpy as np
import requests
import pickle

data = pd.read_csv('../../../data/2_crops_suitable/processed/preprocessed_700.csv')

# Remove  columns "pH and Yield" from the dataframe
data.drop(['pH', 'Yield'], axis=1, inplace=True)

# Remove rows having null values
data.dropna(axis=0, inplace=True)