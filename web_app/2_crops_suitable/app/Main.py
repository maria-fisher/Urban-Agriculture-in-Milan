import streamlit as st
from PIL import Image
import base64

# Set the page layout
st.set_page_config(layout="wide")


# Set background image
#set_background(r'C:\Users\rampr\Documents\Urban-Agriculture-in-Milan\web_app\2_crops_suitable\app\media\crop.png')  # Replace 'background.png' with the path to your background image

# Title and introduction
st.title("🌱 Welcome to the Urban Farming Prediction App")
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

**Note**: Ensure all input fields are filled accurately for the best prediction results.
""")

# Visualization and Reports
st.header("📊 Data Visualization and Reports")
st.markdown("""
We provide comprehensive visualizations to help you make informed decisions. Explore the following:
- **🔍 Heatmaps**: Understand the correlation between different environmental factors.
- **📊 Histograms**: Analyze the distribution of various attributes.
- **📈 Boxplots**: Identify outliers and understand data spread.
- **📉 Scatter Plots**: Visualize relationships between variables.
- **📈 Line Plots**: Track changes and trends over time.

### Embedded Looker Studio Report
Get detailed insights and analytics through our integrated Looker Studio report.
""")

# Contact and Feedback
st.header("📧 Contact and Feedback")
st.markdown("""
We value your feedback! If you have any questions, suggestions, or encounter any issues, please reach out to us at [contact email].

### Feedback Form
[Link to a feedback form] to share your thoughts and suggestions.
""")

# Footer
st.markdown("""
## Developed by the Omdena Milan Chapter Team
For more information, visit our [LinkedIn page](https://www.linkedin.com/company/omdena-milan-chapter/).
""")
