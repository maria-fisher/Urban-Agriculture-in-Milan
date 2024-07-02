import streamlit as st
import pandas as pd
import numpy as np
from predict_unsupervised import predict_unsupervised
from data_fetcher import DataFetcher

def app():
    st.title("Unsupervised Model Prediction")
    
    st.write("""
    Enter the latitude and longitude to predict whether the area is suitable for agriculture.
    """)
    
    latitude = st.number_input("Latitude", format="%.6f", key = "<sort1>")
    longitude = st.number_input("Longitude", format="%.6f", key = "<sort2>")
    
    st.write("Entered Latitude:", latitude)
    st.write("Entered Longitude:", longitude)
    
    map_data = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})
    st.write("Location on Map:")
    st.map(map_data)
    
    if st.button("Predict"):
        prediction = predict_unsupervised(latitude, longitude)
        
    if st.button("Go back"):
        st.session_state.page = "main"
        st.rerun()

if __name__ == "__main__":
    app()