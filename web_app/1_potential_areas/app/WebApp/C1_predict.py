import streamlit as st
import pickle
import numpy as np
import pandas as pd
import folium
from streamlit_folium import folium_static

# Load the models (adjust paths as necessary)
with open('models/XGBClassifier_Pipeline_Optuna_Vidhi.pkl', 'rb') as f:
    supervised_model = pickle.load(f)

with open('models/kmeans_model_pipeline.pkl', 'rb') as f:
    unsupervised_model = pickle.load(f)

# Function to get prediction
def get_prediction(model, features):
    if isinstance(model, type(supervised_model)):
        return model.predict(features)[0]
    elif isinstance(model, type(unsupervised_model)):
        return model.predict(features)[0]

# Function to display the Streamlit app
def run_app():
    # Custom CSS for title
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playwrite+US+Modern:wght@100..400&display=swap');
        .custom-title {
            font-family: 'Playwrite US Modern', sans-serif;
            font-size: 2em;
            color: #556B2F; /* Olive green color */
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button("Go back"):
        st.session_state.page = "main"
        st.rerun()
    

    # Title with custom font and color
    st.markdown('<p class="custom-title">Urban Farming Suitability Prediction</p>', unsafe_allow_html=True)

    
    # Input fields arranged in rows of four
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        latitude = st.number_input('Latitude')
    with col2:
        longitude = st.number_input('Longitude')
    with col3:
        roughness = st.number_input('Roughness')
    with col4:
        slope = st.number_input('Slope')

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        ndvi = st.number_input('NDVI')
    with col6:
        smi = st.number_input('SMI')
    with col7:
        ndwi = st.number_input('NDWI')
    with col8:
        savi = st.number_input('SAVI')

    col9, col10, col11 = st.columns(3)
    with col9:
        landuse = st.selectbox('Landuse', ['railway', 'residential', 'grass', 'farmland', 'military',
                                           'meadow', 'recreation_ground', 'construction', 'industrial',
                                           'commercial', 'retail', 'farmyard', 'village_green', 'brownfield',
                                           'religious', 'flowerbed', 'allotments', 'forest', 'garages',
                                           'depot', 'orchard', 'quarry', 'churchyard',
                                           'greenhouse_horticulture', 'old_cementery', 'plant_nursery',
                                           'cemetery', 'basin'])
    with col10:
        solar_radiation = st.number_input('Solar Radiation')
    with col11:
        ndbi = st.number_input('NDBI')
    
    st.write("Location on Map:")
    
    map_data = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})
    
    def create_map(latitude, longitude, zoom=10):
        m = folium.Map(location=[latitude, longitude], zoom_start=zoom)
        folium.Marker([latitude, longitude]).add_to(m)
        return m

    map = create_map(latitude, longitude)
    folium_static(map)

    # Model selection
    model_type = st.selectbox('Select Model', ['Supervised Model : XGBClassifier', 'Unsupervised Model : KmeansClassifier'])

    # Model mapping
    model = supervised_model if model_type == 'Supervised Model : XGBClassifier' else unsupervised_model

    # Predict button
    if st.button('Predict'):
        if model_type == 'Supervised Model : XGBClassifier':
            features = pd.DataFrame({
                'SMI': [smi],
                'NDBI': [ndbi],
                'Roughness': [roughness],
                'Zone': ["zone4"],
                'Slope': [slope],
                'NDVI': [ndvi],
                'LST': [121.681648448277],
                'NDWI': [ndwi],
                'SAVI': [savi],
                'landuse': [landuse],
                'solar_radiation': [solar_radiation],
                'Longitude': [longitude],
                'Latitude': [latitude]
            })
            prediction = model.predict(features)[0]
            suitability = 'Suitable' if prediction == 1 else 'Not Suitable'
        else:  # Unsupervised Model : KmeansClassifier
            features = pd.DataFrame({
                'SMI': [smi],
                'NDBI': [ndbi],
                'Roughness': [roughness],
                'Slope': [slope],
                'NDVI': [ndvi],
                'LST': [121.681648448277],
                'NDWI': [ndwi],
                'SAVI': [savi],
                'landuse': [landuse],
                'solar_radiation': [solar_radiation],
                'longitude': [longitude],
                'latitude': [latitude],
                'Zone': ["zone4"]
            })
            prediction = model.predict(features)[0]
            suitability = 'Not Suitable' if prediction in [0, 2] else 'Suitable'

        st.write(f'The land is {suitability} for Urban Farming.')

if __name__ == '__main__':
    run_app()

