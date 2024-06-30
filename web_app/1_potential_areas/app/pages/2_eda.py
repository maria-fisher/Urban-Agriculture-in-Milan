import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Function for EDA/Dashboards/Features Used Page
def eda_page():
    
    col1, col2, col3, col4 = st.columns([1,1,3,1], gap='medium')
    with col1:
        st.page_link(r"pages/1_home.py", label="Home", icon="🏠")
    with col2:
        st.page_link(r"pages/2_eda.py", label="EDA", icon="📶")
    with col3:
        st.page_link(r"pages/3_prediction.py", label="Find Suitable Area for Uraban Farming", icon="🤖")
    with col4:
        st.page_link(r"pages/4_contact.py", label="Contact Us", icon="📧")

    # st.set_page_config(page_icon=':bar_chart:')
    st.title("Exploratory Data Analysis")
    st.header("Feature Distributions and Data Sources")

    st.write("Here are the features used in the model along with their distributions:")

    # Data to simulate EDA
    df = pd.read_csv(r"E:\DS\Projects\Omdena_Milano\Urban-Agriculture-in-Milan\data\1_potential_areas\processed\Nitesh_2014_and_2023\Data_2014\Final_combined_data_Zone4_with_target_v2.csv")
    st.map(df, latitude='col1', longitude='col2', size='col3', color='col4')

    # Display plots of each feature
    
    st.write("""
    Data was collected from various sources such as satellite imagery, geographical surveys, and climate databases.
    Techniques used include remote sensing, GIS analysis, and environmental monitoring.
    """)

if __name__ == "__main__":
    eda_page()