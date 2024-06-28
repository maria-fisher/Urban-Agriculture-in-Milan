import streamlit as st
import pandas as pd
import numpy as np
import pickle
from pathlib import Path


def load_model(model_path):
    """Function to load a model from a given path."""
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Function to preprocess inputs
def preprocess_inputs(longitude, latitude, landuse, NDVI, NDBI, NDWI, Roughness, SAVI, Slope, SMI, solar_radiation):
    # Create a DataFrame with the inputs
    data = {
        'longitude': [longitude],
        'latitude': [latitude],
        'landuse': [landuse.lower()],
        'NDVI': [NDVI],
        'NDBI': [NDBI],
        'NDWI': [NDWI],
        'Roughness': [Roughness],
        'SAVI': [SAVI],
        'Slope': [Slope],
        'SMI': [SMI],
        'solar_radiation': [solar_radiation]
    }
    df = pd.DataFrame(data)

    return df

def display_classification_result(prediction, prediction_proba):
    """Function to display the classification result and probabilities."""
    st.subheader("Classification Result")
    if prediction[0] == 1:
        st.success("The area is suitable for urban farming!")
        st.subheader("Prediction Probability")
        st.write(f"Probability of being suitable: {prediction_proba[0][1]:.2f}")
    else:
        st.error("The area is not suitable for urban farming.")
        st.subheader("Prediction Probability")
        st.write(f"Probability of being not suitable: {prediction_proba[0][0]:.2f}")

def display_clustering_result(cluster):
    """Function to display the clustering result."""
    st.subheader("Clustering Result")
    if cluster[0] == 1:
        st.write("The area is suitable for urban farming!")
    else:
        st.error("The area is not suitable for urban farming.")

# Function for Model/Prediction Page
def prediction_page():
    col1, col2, col3, col4 = st.columns([1,1,3,1], gap='medium')

    with col1:
        st.page_link(r"pages/1_home.py", label="Home", icon="🏠")
    with col2:
        st.page_link(r"pages/2_eda.py", label="EDA", icon="📶")
    with col3:
        st.page_link(r"pages/3_prediction.py", label="Find Suitable Area for Uraban Farming", icon="🤖")
    with col4:
        st.page_link(r"pages/4_contact.py", label="Contact Us", icon="📧")

    # st.set_page_config()
    st.header("Urban Farming Suitability Prediction")

    st.subheader("Input Features")

    # Numerical Inputs 
    NDVI, NDBI, NDWI, Roughness, SAVI, Slope, SMI, solar_radiation = [0]*8
    # Categorical Inputs
    landuse = ''

    landuse_catgories = ['farmland', 'allotments', 'residential', 'industrial',
                    'grass', 'farmyard', 'meadow', 'forest', 'construction',
                    'commercial', 'village_green', 'railway', 'retail',
                    'plant_nursery', 'brownfield', 'recreation_ground', 'religious']
    landuse_catgories = [str.capitalize(landuse_catgory) for landuse_catgory in landuse_catgories]

    # Take inputs from user
    col1, col2, col3 = st.columns(3)

    with col1:
        longitude = st.number_input("Longitude", min_value=9.096116, max_value=9.351058, step=0.00000000000001, format="%.15f")
        latitude = st.number_input("Latitude", min_value=45.354995, max_value=45.535018, step=0.00000000000001, format="%.15f")
        landuse = st.selectbox("Landuse Type", landuse_catgories)
        NDVI = st.number_input("NDVI", min_value=-1.0, max_value=1.0, step=0.0000001, format="%.7f")
    
    with col2:
        NDBI = st.number_input("NDBI", min_value=-1.0, max_value=1.0, step=0.0000001, format="%.7f")
        NDWI = st.number_input("NDWI", min_value=-1.0, max_value=1.0, step=0.0000001, format="%.7f")
        Roughness = st.number_input("Roughness", min_value=0.0, max_value=10.0, step=0.1)
        SAVI = st.number_input("SAVI", min_value=-1.0, max_value=1.0, step=0.0000001, format="%.7f")
    
    with col3:
        Slope = st.number_input("Slope", min_value=0.0, max_value=90.0, step=0.0000001, format="%.7f")
        SMI = st.number_input("SMI", min_value=-1.0, max_value=1.0, step=0.0000001, format="%.7f")
        solar_radiation = st.number_input("Solar Radiation", min_value=0.0, max_value=1000.0, step=1.0)

    # Add model selection
    models = ["Supervised Model: XGBClassifier", "Unsupervised Model: K-means Clustering"]
    model_choice = st.selectbox("Select Model", models)

    if st.button("Classify"):
        input_data = preprocess_inputs(latitude, longitude, landuse, NDVI, NDBI, NDWI, Roughness, SAVI, Slope, SMI, solar_radiation)
        models_dir = Path("models")
        if model_choice == models[0]:
            # Load pre-trained XGBClassifier model
            model_path = models_dir.joinpath('urban_farming_supervised_model.pkl')
            model = load_model(model_path)
            prediction = model.predict(input_data)
            prediction_proba = model.predict_proba(input_data)
            display_classification_result(prediction, prediction_proba)

        elif model_choice == models[1]:
            # Load K-means model
            model_path = models_dir.joinpath('kmeans_model.pkl')
            model = load_model(model_path)
            cluster = model.predict(input_data)
            display_clustering_result(cluster)


if __name__ == "__main__":
    prediction_page()