import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Crop Selection and Yield Prediction for Urban Farming in Milan",
    page_icon="🌿",
    layout="wide",
)

# Title and Sidebar
st.title("🌿 Crop Selection and Yield Prediction for Urban Farming in Milan")
st.sidebar.title('📊 Crop and Yield Prediction Dashboard')
st.sidebar.image("./media/omdena_milan.png", use_column_width='always')

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
    padding: 10px 0;
    box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
}
</style>
<div class="footer">
    <p>Developed with <span style='color:red;'>❤</span> by <a href="https://www.linkedin.com/company/omdena-milan-chapter/" target="_blank">Omdena-Milan Chapter Team</a></p>
</div>
""", unsafe_allow_html=True)
