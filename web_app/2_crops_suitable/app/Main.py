import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import base64
from PIL import Image
from streamlit_option_menu import option_menu
from utils import utils
from st_pages import Page, show_pages, add_page_title
from pathlib import Path

root_path = Path(__file__).parent
media_path = root_path.joinpath("media")
pages_path = root_path.joinpath('Pages')

st.set_page_config(
    page_title="Crop Selection and Yield Prediction for Urban Farming in Milan",
    page_icon="🏚️",
    layout="wide",
    )
# Sidebar image
st.sidebar.image(str(media_path.joinpath("omdena_logo_navigation.png")), use_column_width='always')

utils.set_custom_bg()
utils.custom_navbar()

# Title and Sidebar
st.title("🌿 Crop Selection and Yield Prediction for Urban Farming in Milan")

# Project Background
st.markdown("""
This application is designed to help urban farmers in Milan identify the best crops to grow and predict their potential yields based on local environmental conditions.
""")

# Overview
st.header("📋 Overview")
st.markdown("""
With this app, you can:
- 🌿 Input various environmental factors specific to your urban farming site.
- 🌾 Get predictions for the most suitable crops to grow.
- 📈 Estimate the potential yield for each crop.
- 📊 Visualize data and insights through interactive charts and reports.
""")

# Key Features
st.header("🔑 Key Features")
st.markdown("""
- **🌱 Crop Suitability Prediction**: Discover which crops are best suited for your urban farming site.
- **🌽 Yield Prediction**: Estimate the potential yield based on environmental conditions.
- **📊 Data Visualization**: Explore interactive charts and graphs to better understand the data.
- **🔬 Comprehensive Analysis**: Take into account various factors like soil quality, light intensity, and more.
""")

# How to Use the App
st.header("📖 How to Use the App")
st.markdown("""
1. **✍️ Enter Environmental Data**: Fill in the required fields with information about your farming site.
2. **🔍 Get Predictions**: Click the 'Predict' button to see the best crops to grow and their expected yields.
3. **📊 Explore Data**: Use the interactive charts and reports to gain deeper insights into the data.
4. **💾 Download Results**: Export your predictions and data visualizations for further analysis.

**Note:** Ensure that all input fields are filled in accurately for the best prediction results.

### Useful Links
- [Omdena](https://omdena.com/)
- [Project GitHub Repository](https://github.com/omdena/milan-urban-farming)
- [Omdena Milan LinkedIn](https://www.linkedin.com/company/omdena-milan-chapter/)

### Contact Us
For more information, please reach out to our team at [email@example.com](mailto:email@example.com) 📧
""")

# Display Image
st.image(str(media_path.joinpath("omdena_logo.jpg")), use_column_width='auto')


show_pages(
    [
        Page(str(root_path.joinpath("Main.py")), "Home", "🏠"),
        Page(str(pages_path.joinpath("EDA.py")), "EDA", ":books:"),
        Page(str(pages_path.joinpath("Crop_Selections.py")), "Crop Selection", "🌿"),
        Page(str(pages_path.joinpath("Yield_Prediction.py")), "Yield Prediction", "🌾")
    ]
)

add_page_title(layout="wide")