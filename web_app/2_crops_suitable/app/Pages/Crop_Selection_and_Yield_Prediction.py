import streamlit as st
import pandas as pd
import numpy as np
import requests
import pickle

data = pd.read_csv('../../../data/2_crops_suitable/processed/preprocessed_700.csv')