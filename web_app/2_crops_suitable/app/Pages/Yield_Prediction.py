main


main
import streamlit as st
import pandas as pd
import numpy as np
import requests
import pickle

main
# Load the trained model
model_path =r"C:\Users\rampr\Documents\Urban-Agriculture-in-Milan\web_app\2_crops_suitable\app\predictingyield.pkl"
with open(model_path, 'rb') as file:
    model = pickle.load(file)
    
    # Title of the app
st.title("Crop Yield Prediction")

# Sidebar for user input parameters
st.sidebar.header("Input Parameters")

def user_input_features():
    crop_type = st.sidebar.selectbox('Crop Name', ('Asparagus', 'Broccoli', 'Cabbage', 'Cauliflowers' ,'Chilly Peppers','Cucumbers','Eggplants','Green Peas','Potatoes','Tomatoes','Apple','Apricot','Blueberry','Cherries','Figs','Grapes','Kiwi','Lemon','Orange','Peach','Pear','Plum','Pomegranate','Strawbwrry','Watermelon','Argula','Beet','Chard','Cress','Endive','Kale','Lettuce','Raddicchio','Spinach' ))
    Fertility = st.sidebar.selectbox('Fertility', ('High', 'Moderate'))
    Photoperiod = st.sidebar.selectbox('Photoperiod', ('Day Neutral', 'Long Day Period','Short Day Period'))
   # feature4 = st.sidebar.number_input('N-P-K Ratio', min_value=0.0, max_value=100.0, value=50.0)
    Temperature = st.sidebar.number_input('Temperature', min_value=0.0, max_value=100.0, value=50.0)
    Rainfall = st.sidebar.number_input('Rainfall', min_value=0.0, max_value=100.0, value=50.0)
   
    Light_Hours = st.sidebar.number_input('Light_Hours', min_value=0.0, max_value=100.0, value=50.0)
    Light_Intensity = st.sidebar.number_input('Light_Intensity', min_value=0.0, max_value=100.0, value=50.0)
    Rh = st.sidebar.number_input('Rh', min_value=0.0, max_value=100.0, value=50.0)
    Nitrogen = st.sidebar.number_input('Nitrogen', min_value=0.0, max_value=100.0, value=50.0)
    Phosphorus = st.sidebar.number_input('Phosphorus', min_value=0.0, max_value=100.0, value=50.0)
    Potassium = st.sidebar.number_input('Potassium', min_value=0.0, max_value=100.0, value=50.0)
    Potassium_Ratio = st.sidebar.number_input('Potassium_Ratio', min_value=0.0, max_value=100.0, value=50.0)
    Phosphorus_Ratio = st.sidebar.number_input('Phosphorus_Ratio', min_value=0.0, max_value=100.0, value=50.0)
    Nitrogen_Ratio = st.sidebar.number_input('Nitrogen_Ratio', min_value=0.0, max_value=100.0, value=50.0)
    Category_pH = st.sidebar.selectbox('Category ph', ('acidic', 'low_acidic','low_alkaline','neutral'))
    Soil_Type = st.sidebar.selectbox('Soil_type', ('Loam', 'Sandy','Sandy_Loam'))
    Season = st.sidebar.selectbox('Season', ('Fall', 'Spring','Summer','Winter'))
    data = {
        'crop_type': crop_type,
        'Fertility': Fertility,
        'Photoperiod': Photoperiod,
        'Rainfall': Rainfall,
        'Temperature': Temperature,
        'Light_Hours': Light_Hours,
        'Light_Intensity': Light_Intensity,
        'Rh': Rh,
        'Nitrogen': Nitrogen,
        'Phosphorus': Phosphorus,
        'Potassium': Potassium,
        'Potassium_Ratio':Potassium_Ratio,
        'Phosphorus_Ratio':Phosphorus_Ratio,
        'Nitrogen_Ratio':Nitrogen_Ratio,
        'Category_pH':Category_pH,
        'Soil_Type':Soil_Type,
        'Season':Season
        
    }
    features = pd.DataFrame(data, index=[0])
    return features

# Get user input
input_df = user_input_features()

# Display user input
st.subheader('User Input Parameters')
st.write(input_df)

# Make prediction
prediction = model.predict(input_df)

# Display prediction in a beautiful box
st.subheader('Predicted Crop Yield')
st.success(f'The predicted crop yield is: {prediction[0]}')


#if __name__ == '__main__':
   # st.run()

data = pd.read_csv('../../../data/2_crops_suitable/processed/preprocessed_700.csv')

# Remove  columns "pH and Yield" from the dataframe
data.drop(['pH', 'Yield'], axis=1, inplace=True)

# Remove rows having null values
data.dropna(axis=0, inplace=True)
main
