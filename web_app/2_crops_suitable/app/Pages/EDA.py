import streamlit as st
import streamlit.components.v1 as components
from st_pages import add_page_title
from utils import utils

def app():
    # Title of the EDA page
    st.title("Exploratory Data Analysis")

    # Looker Studio report URL
    report_url = "https://lookerstudio.google.com/embed/reporting/308794df-40c2-4857-a909-ab689dbcfb3e/page/p_iluq9g1zhd"

    # Create the iframe HTML
    iframe_code = f"""
    <iframe width="100%" height="1000" src="{report_url}" frameborder="0" style="border:0" allowfullscreen></iframe>
    """

    # Display the iframe using Streamlit's components.html function
    components.html(iframe_code, height=1000)

utils.set_custom_bg()
utils.custom_navbar()
# Sidebar image
st.sidebar.image("./media/omdena_logo_navigation.png", use_column_width='always')
app()
add_page_title(layout="wide")