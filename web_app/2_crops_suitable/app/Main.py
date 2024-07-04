import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import base64
from PIL import Image
from streamlit_option_menu import option_menu
from utils import utils
from st_pages import Page, show_pages, add_page_title

st.set_page_config(
    page_title="Crop Selection and Yield Prediction for Urban Farming in Milan",
    page_icon="🏚️",
    layout="wide",
    )
# Sidebar image
st.sidebar.image("./media/omdena_logo_navigation.png", use_column_width='always')

utils.set_custom_bg()
utils.custom_navbar()

# Title and Sidebar
st.title("🌿 Crop Selection and Yield Prediction for Urban Farming in Milan")

# Project Background
st.markdown("""
## Project Background

### Challenge Background

### Project Goals
- 🎯 **Develop an algorithm** that takes into account the environmental conditions, location, and available infrastructure to predict the potential growth of crops in urban areas.
- 📊 **Analyze factors** such as sunlight exposure, soil quality, water availability, and temperature to determine the most suitable crops for a specific urban farming site.
- 📋 **Address the risks** associated with urban farming to ensure a successful and sustainable operation. Minimize potential risks related to urban agriculture, including health risks from wastewater irrigation, trace metal, zoonotic risks, and other health risks.
- 📣 **Suggest solutions** to potential urban farmers to create a safe and productive environment for growing crops in urban settings.

### How to Use This App
1. 👉 Navigate to the [**Model**](#model) page.
2. ✍️ Enter the required input features.
3. 📈 Get predictions for crop and yield for the input features.

**Note:** Ensure that all input fields are filled in accurately for the best prediction results.

### Useful Links
- [Omdena](https://omdena.com/)
- [Project GitHub Repository](https://github.com/omdena/milan-urban-farming)
- [Omdena Milan LinkedIn](https://www.linkedin.com/company/omdena-milan-chapter/)

### Contact Us
For more information, please reach out to our team at [email@example.com](mailto:email@example.com) 📧
""")

# Display Image
st.image("./media/omdena_logo.jpg", use_column_width='auto')


show_pages(
    [
        Page("main.py", "Home", "🏠"),
        Page("pages/EDA.py", "EDA", ":books:"),
        Page("pages/Crop_Selections.py", "Crop Selection", "🌿"),
        Page("Pages/Yield_Prediction.py", "Yield Prediction", "🌾")
    ]
)

add_page_title(layout="wide")