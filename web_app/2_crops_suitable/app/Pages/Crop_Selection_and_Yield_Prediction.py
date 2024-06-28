import streamlit as st
import pandas as pd
import numpy as np
import requests
import pickle

# data = pd.read_csv('../../../data/2_crops_suitable/processed/preprocessed_700.csv')

st.title("Crop Selection and Yield Prediction")

st.markdown(
    """
### Enter the required features to predict the suitable crop and yield information.
Please provide the values for the following features:
"""
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    Fertility = st.multiselect("Fertility", ["High", "Moderate"])
    Photoperiod = st.multiselect(
        "Photoperiod", ["Day Neutral", "Long Day Period", "Short Day Period"]
    )
    NPKRatio = st.multiselect(
        "N-P-K Ratio",
        [
            "5:10:05",
            "5:10:10",
            "6:06:06",
            "8:15:36",
            "10:10:05",
            "10:10:10",
            "13:13:13",
            "20:10:20",
            "22:12:13",
            "75:37.5:37.5",
        ],
    )
    Temperature = st.number_input(
        "Temperature", min_value=10.00, max_value=40.00, help=""
    )
    Rainfall = st.number_input("Rainfall", min_value=400.00, max_value=2800.00, help="")
    Light_Hours = st.number_input(
        "Light_Hours", min_value=5.00, max_value=30.00, help=""
    )
    Light_Intensity = st.number_input(
        "Light_Intensity", min_value=50.00, max_value=1200.00, help=""
    )

with col2:
    Rh = st.number_input("Rh", min_value=50.00, max_value=100.00, help="")
    Nitrogen = st.number_input("Nitrogen", min_value=40.00, max_value=400.00, help="")
    Phosphorus = st.number_input(
        "Phosphorus", min_value=20.00, max_value=300.00, help=""
    )
    Potassium = st.number_input("Potassium", min_value=30.00, max_value=300.00, help="")
    Category_pH = st.multiselect(
        "Category_pH", ["acidic", "low_acidic", "low_alkaline", "neutral"]
    )
    Soil_Type = st.multiselect("Soil_type", ["Loam", "Sandy", "Sandy Loam"])
    Season = st.multiselect("Season", ["Fall", "Spring", "Summer", "Winter"])

Nitrogen_Ratio = []
Phosphorus_Ratio = []
Potassium_Ratio = []

for data in NPKRatio:
    ratio = data.split(":")
    Nitrogen_Ratio.append(float(ratio[0]))
    Phosphorus_Ratio.append(float(ratio[1]))
    Potassium_Ratio.append(float(ratio[2]))


input_data = {
    "Fertility": [Fertility],
    "Photoperiod": [Photoperiod],
    "Temperature": [Temperature],
    "Rainfall": [Rainfall],
    "Light_Hours": [Light_Hours],
    "Light_Intensity": [Light_Intensity],
    "Rh": [Rh],
    "Nitrogen": [Nitrogen],
    "Phosphorus": [Phosphorus],
    "Potassium": [Potassium],
    "Category_pH": [Category_pH],
    "Soil_Type": [Soil_Type],
    "Season": [Season],
    "Nitrogen_Ratio": [Nitrogen_Ratio],
    "Phosphorus_Ratio": [Phosphorus_Ratio],
    "Potassium_Ratio": [Potassium_Ratio],
}

input_df = pd.DataFrame(input_data, index=[0])
# st.button("Predict")

if st.button("Predict"):
    try:
        with open("./cropselection.pkl", "rb") as file:
            pipeline = pickle.load(file)

        st.write("**You have submitted the below data.**")
        st.write(input_df)
        prediction = pipeline.predict(input_df)
        # st.success(f"Predicted Crop: {prediction[0]}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
