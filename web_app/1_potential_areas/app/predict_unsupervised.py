import pandas as pd
import streamlit as st
from handler import DataFetcher, load_model
from pathlib import Path

# PATH
root_path = Path(__file__).parent.parent.parent.parent
task_path = root_path.joinpath("web_app/1_potential_areas/app")
models_path = task_path.joinpath("models")
data_path = task_path.joinpath("dataset")

# Load the trained model
model = load_model(models_path.joinpath("kmeans_model_pipeline.pkl"))

# Initialize DataFetcher
data_fetcher = DataFetcher(data_path.joinpath('MergedData_2023.parquet'))

def predict_unsupervised(latitude, longitude):
    # Fetch additional data based on latitude and longitude
    additional_data = data_fetcher.fetch_data(latitude, longitude)

    if additional_data is None:
        st.error("No data found for the given latitude and longitude.")
    else:
        # Prepare the input data for the model as a Pandas DataFrame
        input_data = pd.DataFrame({
            'latitude': [latitude],
            'longitude': [longitude],
            'Zone': [additional_data['Zone']],
            'NDVI': [additional_data['NDVI']],
            'landuse': [additional_data['landuse']],
            'LST': [additional_data['LST']],
            'NDBI': [additional_data['NDBI']],
            'NDWI': [additional_data['NDWI']],
            'Roughness': [additional_data['Roughness']],
            'SAVI': [additional_data['SAVI']],
            'Slope': [additional_data['Slope']],
            'SMI': [additional_data['SMI']],
            'solar_radiation': [additional_data['solar_radiation']]
        })

        # Write the additional features with custom styling
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Playwrite+DE+Grund:wght@100..400&family=Teko:wght@300..700&display=swap');
            .custom-text {
                font-family: 'Teko', sans-serif;
                font-size: 1.5em;
                color: #556B2F; /* Olive green color */
                font-weight: 500;
            }
            .big-bold-text {
                font-size: 1.8em;
                font-weight: bold;
                color: #D9534F; /* Bootstrap error color */
            }
            .big-bold-success {
                font-size: 1.8em;
                font-weight: bold;
                color: #5CB85C; /* Bootstrap success color */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.write("### Additional Features:")
        features = [
            ('Zone', f"{additional_data['Zone']}"),
            ('NDVI', f"{additional_data['NDVI']:.6f}"),
            ('Land Use', f"{additional_data['landuse']}"),
            ('LST', f"{additional_data['LST']:.6f}"),
            ('NDBI', f"{additional_data['NDBI']:.6f}"),
            ('NDWI', f"{additional_data['NDWI']:.6f}"),
            ('Roughness', f"{additional_data['Roughness']:.6f}"),
            ('SAVI', f"{additional_data['SAVI']:.6f}"),
            ('Slope', f"{additional_data['Slope']:.6f}"),
            ('SMI', f"{additional_data['SMI']:.6f}"),
            ('Solar Radiation', f"{additional_data['solar_radiation']:.6f}")
        ]

        cols = st.columns(3)
        for i, (name, value) in enumerate(features):
            cols[i % 3].write(f"<span class='custom-text'>{name}: {value}</span>", unsafe_allow_html=True)
        
        # Make the prediction
        prediction = model.predict(input_data)

        if prediction[0] == 1:
            st.markdown("<p class='big-bold-success'>The area is Suitable for Urban Farming</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p class='big-bold-text'>The area is Not Suitable for Urban Farming</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    st.title("Agricultural Suitability Prediction")
    latitude = st.number_input("Enter Latitude", format="%.6f")
    longitude = st.number_input("Enter Longitude", format="%.6f")
    if st.button("Predict"):
        predict_unsupervised(latitude, longitude)


