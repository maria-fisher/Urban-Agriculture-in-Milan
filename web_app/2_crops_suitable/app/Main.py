import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


st.title("Crop Selection and Yield Prediction for Urban Farming in Milan")
st.sidebar.title('Crop and Yield Prediction Dashboard')
st.sidebar.image("./media/omdena_milan.png", use_column_width='never') 
st.markdown("""
## Project Background


### Challenge Background


### Project Goals
- :dart: **Develop an algorithm that takes into account the environmental conditions, location, and available infrastructure to predict the potential growth of crops in urban areas. 
- :bar_chart: **Analyze facltors such as sunlight exposure, soil quality, water availability and temperature to determine the most suitable crops for a specific urban farming site.
- :clipboard: **Address the risks associated with urban farming to ensure a successful and sustainable operation. Minimise potential risks related to urban agriculture, social and economic risks, including health risks from wastewater irrigation, trace metal, zoonotic risks, and other health risks.**
- :mega: **By identifying and mitigating these risks, we can suggest solutions to potential urban farmers to create a safe and productive environment for growing crops in urban settings.**

### How to Use This App
1. :point_right: Navigate to the [**Model**](#model) page.
2. :writing_hand: Enter the required input features.
3. :chart_with_upwards_trend: Get prediction for crop and yield for input features.

**Note:** Ensure that all input fields are filled in accurately for the best prediction results.

### Useful Links
- 
- 
- 
- 

### Contact Us
For more information, please reach out to our team at [](mailto:) :email:
""")

# df = pd.read_csv('../../../data/2_crops_suitable/processed/preprocessed_700.csv')
# print ("Dataset Length: ", len(df))
# print ("Dataset Shape: ", df.shape)
# # Remove unwanted columns "pH" and "Yield" from the dataframe
# df.drop(['pH', 'Yield'], axis=1, inplace=True)

# # Remove rows having null values
# df.dropna(axis=0, inplace=True)

st.image("./media/omdena_logo.jpg", use_column_width=False)
# Footer
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
}
</style>
<div class="footer">
<p>Developed with <span style='color:blue;'>❤</span> by <a href="https://www.linkedin.com/company/omdena-milan-chapter/" target="_blank">Omdena-Milan Chapter Team</a> </p>
</div>
""", unsafe_allow_html=True)





