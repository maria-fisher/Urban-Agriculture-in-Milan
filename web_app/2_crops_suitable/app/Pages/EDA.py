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
    return pd.read_csv("../../../data/2_crops_suitable/processed/preprocessed_700.csv")


# Define a function to display EDA graphs
def display_eda(data):
    st.title("Exploratory Data Analysis")

    # Pairplot
    st.subheader("Pairplot")
    pairplot_fig = sns.pairplot(data)
    st.pyplot(pairplot_fig)

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    plt.figure(figsize=(10, 4))
    heatmap_fig = sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
    st.pyplot(heatmap_fig.figure)

    # Histogram
    st.subheader("Histogram")
    column = st.selectbox("Select a column for histogram", data.columns)
    hist_fig = px.histogram(data, x=column)
    st.plotly_chart(hist_fig)

    # Boxplot
    st.subheader("Boxplot")
    column = st.selectbox("Select a column for boxplot", data.columns)
    box_fig = px.box(data, y=column)
    st.plotly_chart(box_fig)

    # Violin Plot
    st.subheader("Violin Plot")
    column = st.selectbox("Select a column for violin plot", data.columns)
    violin_fig = px.violin(data, y=column)
    st.plotly_chart(violin_fig)

    # Scatter Plot
    st.subheader("Scatter Plot")
    x_column = st.selectbox("Select x column for scatter plot", data.columns)
    y_column = st.selectbox("Select y column for scatter plot", data.columns)
    scatter_fig = px.scatter(data, x=x_column, y=y_column)
    st.plotly_chart(scatter_fig)

    # Line Plot
    st.subheader("Line Plot")
    line_x_column = st.selectbox("Select x column for line plot", data.columns)
    line_y_column = st.selectbox("Select y column for line plot", data.columns)
    line_fig = px.line(data, x=line_x_column, y=line_y_column)
    st.plotly_chart(line_fig)


# Load data
data = load_data()

# Display EDA graphs
display_eda(data)
