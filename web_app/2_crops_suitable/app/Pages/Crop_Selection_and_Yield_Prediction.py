import streamlit as st
import pandas as pd
import pickle

# Set page configuration
st.set_page_config(
    page_title="Crop and Yield Prediction",
    page_icon="🌾",
    layout="wide",
)

# Title
st.title("🌾 Crop Selection and Yield Prediction for Urban Farming in Milan")

# Sidebar image
#st.sidebar.image("./media/omdena_milan.png", use_column_width='always')

# Layout columns
col1, col2 = st.columns(2)

# Input fields in the first column
with col1:
    Fertility = st.selectbox('Fertility', ('High', 'Moderate'))
    Photoperiod = st.selectbox('Photoperiod', ('Day Neutral', 'Long Day Period', 'Short Day Period'))
    Temperature = st.number_input('Temperature (°C)', min_value=0.0, max_value=100.0, value=31.0)
    Rainfall = st.number_input('Rainfall (mm)', min_value=0.0, max_value=2000.0, value=964.0)
    Light_Hours = st.number_input('Light Hours', min_value=0.0, max_value=100.0, value=14.0)
    Light_Intensity = st.number_input('Light Intensity (µmol/m²/s)', min_value=0.0, max_value=900.0, value=705.0)
    Season = st.selectbox('Season', ('Fall', 'Spring', 'Summer', 'Winter'))

# Input fields in the second column
with col2:
    Rh = st.number_input('Relative Humidity (%)', min_value=0.0, max_value=100.0, value=91.0)
    Nitrogen = st.number_input('Nitrogen (kg/ha)', min_value=0.0, max_value=200.0, value=156.0)
    Phosphorus = st.number_input('Phosphorus (kg/ha)', min_value=0.0, max_value=100.0, value=70.0)
    Potassium = st.number_input('Potassium (kg/ha)', min_value=0.0, max_value=300.0, value=225.0)
    NPKRatio = st.selectbox("N-P-K Ratio", ["5:10:05", "5:10:10", "6:06:06", "8:15:36", "10:10:05", "10:10:10", "13:13:13", "20:10:20", "22:12:13", "75:37.5:37.5"])
    Category_pH = st.selectbox('Category pH', ('neutral', 'acidic', 'low_alkaline' ,'low_acidic'))
    Soil_Type = st.selectbox('Soil Type', ('Loam', 'Sandy', 'Sandy Loam'))

# Split the N-P-K ratio
ratio = NPKRatio.split(':')
Nitrogen_Ratio = float(ratio[0])
Phosphorus_Ratio = float(ratio[1])
Potassium_Ratio = float(ratio[2])

# Prepare input data
input_data = {
    'Fertility': Fertility,
    'Photoperiod': Photoperiod,
    'Temperature': Temperature,
    'Rainfall': Rainfall,
    'Light_Hours': Light_Hours,
    'Light_Intensity': Light_Intensity,
    'Rh': Rh,
    'Nitrogen': Nitrogen,
    'Phosphorus': Phosphorus,
    'Potassium': Potassium,
    'Category_pH': Category_pH,
    'Soil_Type': Soil_Type,
    'Season': Season,
    'Nitrogen_Ratio': Nitrogen_Ratio,
    'Phosphorus_Ratio': Phosphorus_Ratio,
    'Potassium_Ratio': Potassium_Ratio
}

# Convert input data to DataFrame
input_df = pd.DataFrame([input_data])

# Load the models
try:
    with open('./classifycrop.pkl', 'rb') as file:
        classify_model = pickle.load(file)
    with open('./predictingyield.pkl', 'rb') as file:
        yield_model = pickle.load(file)

    # Ensure all expected columns are present
    expected_columns_classify = classify_model.feature_names_in_
    expected_columns_yield = yield_model.feature_names_in_

    # Initialize missing columns with zeros for classification model
    for col in expected_columns_classify:
        if col not in input_df.columns:
            input_df[col] = 0  # or a default value

    # Ensure the column order matches the classification model's expected input
    input_df_classify = input_df[expected_columns_classify]

    # Prediction button
    if st.button("Predict"):
        # Predict the crop type
        crop_prediction = classify_model.predict(input_df_classify)
        st.subheader('Predicted Crop')
        st.write(f"🌿 **Predicted Crop:** {crop_prediction[0]}")

        # Prepare input for yield prediction
        input_df['Predicted_Crop'] = crop_prediction[0]

        # Initialize missing columns with zeros for yield model
        for col in expected_columns_yield:
            if col not in input_df.columns:
                input_df[col] = 0  # or a default value

        # Ensure the column order matches the yield model's expected input
        input_df_yield = input_df[expected_columns_yield]

        # Predict the yield
        yield_prediction = yield_model.predict(input_df_yield)
        st.subheader('Predicted Crop Yield')
        st.write(f"🌾 **Predicted Yield:** {yield_prediction[0]} tons per hectare")

except Exception as e:
    st.error(f"An error occurred: {e}")
