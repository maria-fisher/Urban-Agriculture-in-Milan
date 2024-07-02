import streamlit as st
import streamlit.components.v1 as components

# Set Streamlit page layout
st.set_page_config(layout="wide")

# Title of the EDA page
st.title("Exploratory Data Analysis")

# Looker Studio report URL
report_url = "https://lookerstudio.google.com/reporting/308794df-40c2-4857-a909-ab689dbcfb3e/page/BjF2D"

# Create the iframe HTML
iframe_code = f"""
<iframe width="100%" height="1000" src="{report_url}" frameborder="0" style="border:0" allowfullscreen></iframe>
"""

# Display the iframe using Streamlit's components.html function
components.html(iframe_code, height=1000)

# Additional EDA content can be added below if needed
st.header("Additional EDA Content")
st.write("You can add more EDA content here.")