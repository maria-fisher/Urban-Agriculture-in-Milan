import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import geopandas as gpd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(layout="wide")

# Root Path
root_path = Path(__file__).parent.parent.parent.parent.parent


# Function for EDA/Dashboards/Features Used Page
def eda_page():
    app_path = "web_app/1_potential_areas/app"
    pages_path = root_path.joinpath(app_path).joinpath("pages")

    col1, col2, col3, col4 = st.columns([1, 1, 3, 1], gap="medium")
    with col1:
        st.page_link(str(pages_path.joinpath("1_home.py")), label="Home", icon="🏠")
    with col2:
        st.page_link(str(pages_path.joinpath("2_eda.py")), label="EDA", icon="📶")
    with col3:
        st.page_link(
            str(pages_path.joinpath("3_prediction.py")),
            label="Find Suitable Area for Uraban Farming",
            icon="🤖",
        )
    with col4:
        st.page_link(
            str(pages_path.joinpath("4_contact.py")), label="Contact Us", icon="📧"
        )

    # st.set_page_config(page_icon=':bar_chart:')
    st.title("Exploratory Data Analysis")
    st.header("Feature Distributions and Data Sources")

    st.write("Here are the features used in the model along with their distributions:")

    # Data to simulate EDA

    # Display distributions of each feature

    st.write(
        """
    Data was collected from various sources such as satellite imagery, geographical surveys, and climate databases.
    Techniques used include remote sensing, GIS analysis, and environmental monitoring.
    """
    )


eda_page()


# Looker Studio report URL
report_url = "https://lookerstudio.google.com/embed/reporting/eaab71cb-575f-4f7c-b9ac-97942e43d017/page/r2W2D"

# Create the iframe HTML
iframe_code = f"""
<iframe width="100%" height="1000" src="{report_url}" frameborder="0" style="border:0" allowfullscreen sandbox="allow-storage-access-by-user-activation allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"></iframe>
"""

# Display the iframe using Streamlit's components.html function
components.html(iframe_code, height=1000)


data_dir = root_path.joinpath("data")
# data_path = '1_potential_areas/processed/Opeyemi'
data_path = "1_potential_areas/processed/"


@st.cache_data
def read_csv(filename, index_col=None):
    df = pd.read_csv(
        data_dir.joinpath(data_path).joinpath(filename),
        index_col=index_col,
        engine="pyarrow",
        dtype_backend="pyarrow",
    )
    return df


# Function to classify vegetation based on NDVI value
def classify_vegetation(ndvi):
    if ndvi < 0.1:
        return "Bare Soil/ Built-up Areas"
    elif 0.1 <= ndvi < 0.2:
        return "Sparse Vegetation"
    elif 0.2 <= ndvi < 0.5:
        return "Moderate Vegetation"
    elif ndvi >= 0.5:
        return "Dense Vegetation"
    else:
        return "null"


@st.cache_data
def plot_histogram(data):
    # Creating a subplot figure with Plotly
    fig = make_subplots(rows=3, cols=3, subplot_titles=[title for _, title in data])

    # Adding histograms to the subplots
    for i, (values, title) in enumerate(data, 1):
        row = (i - 1) // 3 + 1
        col = (i - 1) % 3 + 1
        fig.add_trace(
            go.Histogram(x=values, name=title, histnorm="density", showlegend=False),
            row=row,
            col=col,
        )

    # Update layout
    fig.update_layout(height=800, width=1000, showlegend=False)
    return fig


# Compute the correlation matrix and plot
@st.cache_data
def plot_correlation(df, cols: list[str]):
    correlation_matrix = df[cols].corr()

    # Create a Plotly heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            colorbar=dict(title="Correlation"),
        )
    )

    # Update layout
    fig.update_layout(width=800, height=700)
    return fig


# Scatter plot of geographical data
def plot_scatter(df):
    selected_zones = st.multiselect(
        "Select Zone(s)", options=["zone4", "zone9"], default=["zone4", "zone9"]
    )
    filtered_df = df[df["Zone"].isin(selected_zones)]
    x_axis = "Longitude"
    y_axis = "Latitude"
    labels = {
        "longitude": "Longitude",
        "latitude": "Latitude",
        "class": "Vegetation Class",
    }
    colors = {"Class1": "blue", "Class2": "green", "Class3": "red"}
    fig = px.scatter(
        filtered_df,
        x=x_axis,
        y=y_axis,
        color="class",
        labels=labels,
        color_discrete_map=colors,
    )

    # Customize the layout
    fig.update_layout(
        legend=dict(title="Vegetation Class"),
        xaxis=dict(title="Longitude"),
        yaxis=dict(title="Latitude"),
        hovermode="closest",
    )
    return fig


# Bar chart
@st.cache_data
def plot_bar(df):
    class_counts = df["class"].value_counts().reset_index()
    class_counts.columns = ["class", "count"]
    x_axis = "class"
    labels = {"class": "Class", "count": "Count"}
    fig = px.bar(
        class_counts,
        x=x_axis,
        y="count",  # Specify the y-axis as the count of each class
        labels=labels,
        color="class",  # Color bars by class
        color_discrete_sequence=["#00b6cb"],
    )
    # Customize the layout
    fig.update_layout(
        xaxis=dict(title="Class"), yaxis=dict(title="Count"), showlegend=False
    )
    return fig


# Read CSVs
# loading ndvi, ndbi and bu(built-up)
data = read_csv("Merged_2014.csv")

# Apply the classification function to the NDVI column and create a class column
data["class"] = data["NDVI"].apply(classify_vegetation)


hist_data = [
    (data["NDVI"], "NDVI Distribution"),
    (data["NDBI"], "NDBI Distribution"),
    (data["NDWI"], "Water Distribution"),
    (data["solar_radiation"], "Sunlight Distribution"),
    (data["SMI"], "Soil Moisture"),
]

# Histogram
with st.expander("Distribution Plots (Histogram)"):
    hist = plot_histogram(hist_data)
    st.plotly_chart(hist)

# Correlation matrix plot
with st.expander("Correlation Matrix of Vegetation Indices"):
    cols = ["NDVI", "NDBI", "NDWI", "solar_radiation", "SMI", "LST"]
    fig = plot_correlation(data, cols)
    st.plotly_chart(fig)

# Scatter plot
with st.expander("Scatter Plot of Geographical Distribution of Vegetation Classes"):
    scatter_vegetation = plot_scatter(data)
    st.plotly_chart(scatter_vegetation, theme="streamlit", use_container_width=True)

# Bar chart
with st.expander("Bar Chart of Distribution of Vegetation Classes"):
    bar_plot = plot_bar(data)
    st.plotly_chart(bar_plot)