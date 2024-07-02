# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 22:24:06 2024

@author: rampr
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def load_data():
    return pd.read_csv('../../../data/2_crops_suitable/processed/preprocessed_700.csv')

# Define a function to display EDA graphs
def display_eda(data):
    st.title("🔍 Exploratory Data Analysis")

    # Correlation Heatmap
    st.subheader("🔵 Correlation Heatmap")
    plt.figure(figsize=(10, 4))
    heatmap_fig = sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
    st.pyplot(heatmap_fig.figure)

    # Histogram
    st.subheader("📊 Histogram")
    column_hist = st.selectbox("Select a column for histogram", data.columns)
    hist_fig = px.histogram(data, x=column_hist)
    st.plotly_chart(hist_fig)

    # Boxplot
    st.subheader("📦 Boxplot")
    column_box = st.selectbox("Select a column for boxplot", data.columns, key="boxplot")
    box_fig = px.box(data, y=column_box)
    st.plotly_chart(box_fig)

    # Violin Plot
    st.subheader("🎻 Violin Plot")
    column_violin = st.selectbox("Select a column for violin plot", data.columns, key="violin")
    violin_fig = px.violin(data, y=column_violin)
    st.plotly_chart(violin_fig)

    # Scatter Plot
    st.subheader("🔹 Scatter Plot")
    x_column_scatter = st.selectbox("Select x column for scatter plot", data.columns, key="scatter_x")
    y_column_scatter = st.selectbox("Select y column for scatter plot", data.columns, key="scatter_y")
    scatter_fig = px.scatter(data, x=x_column_scatter, y=y_column_scatter)
    st.plotly_chart(scatter_fig)

    # Line Plot
    st.subheader("📈 Line Plot")
    line_x_column = st.selectbox("Select x column for line plot", data.columns, key="line_x")
    line_y_column = st.selectbox("Select y column for line plot", data.columns, key="line_y")
    line_fig = px.line(data, x=line_x_column, y=line_y_column)
    st.plotly_chart(line_fig)

# Load data
data = load_data()

# Display EDA graphs
display_eda(data)
