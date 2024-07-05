import streamlit as st
import pandas as pd
from predict_supervised import predict as predict_supervised
from predict_unsupervised import predict_unsupervised
from data_fetcher import DataFetcher
import folium
from streamlit_folium import folium_static

def app():
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

        .custom-text {
            font-family: "Playwrite DE Grund", sans-serif;
            font-size: 1.1em;
            color: #432818; /* Change the color to #8B4513 */
            text-align: justify;
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
    st.markdown('<p class="custom-text"> Enter the latitude and longitude to predict whether the area is suitable for agriculture.</p>', unsafe_allow_html=True)
    st.markdown('<p class="custom-text"> Note : This feature is only available for Zone 4 and Zone 9 of Milan, Italy.</p>', unsafe_allow_html=True)

    # st.write("""
    # Enter the latitude and longitude to predict whether the area is suitable for agriculture.
    # """)
    # st.write("""
    # Note : This feature is only available for Zone 4 and Zone 9 of Milan, Italy.
    # """)
    
    
    latitude = st.number_input("Latitude", format="%.15f", key="<sort1>")
    longitude = st.number_input("Longitude", format="%.15f", key="<sort2>")

    
    st.write("Entered Latitude:", latitude)
    st.write("Entered Longitude:", longitude)
    
    map_data = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})
    
    def create_map(latitude, longitude, zoom=10):
        m = folium.Map(location=[latitude, longitude], zoom_start=zoom)
        folium.Marker([latitude, longitude]).add_to(m)
        return m

    # Use your latitude and longitude values
    map = create_map(latitude, longitude)
    folium_static(map)
    
    model_type = st.selectbox('Select Model', ['Supervised Model : XGBClassifier', 'Unsupervised Model : KmeansClassifier'])

    if st.button('Predict'):
        if model_type == 'Supervised Model : XGBClassifier':
            prediction = predict_supervised(latitude, longitude)
        else:
            prediction = predict_unsupervised(latitude, longitude)

if __name__ == "__main__":
    app()
