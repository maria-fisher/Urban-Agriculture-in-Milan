import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pathlib import Path

# Root Path
root_path = Path(__file__).parent.parent.parent.parent.parent

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
    fig.update_layout(
        height=800, width=1000, title_text="Distribution Plots", showlegend=False
    )
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
    fig.update_layout(
        title="Correlation Matrix of Vegetation Indices", width=800, height=700
    )
    return fig

# Scatter plot of geographical data
@st.cache_data
def plot_scatter(df):
    x_axis = "Longitude"
    y_axis = "Latitude"
    title = "Geographical Distribution of Vegetation Classes"
    labels = {
        "longitude": "Longitude",
        "latitude": "Latitude",
        "class": "Vegetation Class",
    }
    colors = {"Class1": "blue", "Class2": "green", "Class3": "red"}
    fig = px.scatter(
        df,
        x=x_axis,
        y=y_axis,
        color="class",
        title=title,
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
    x_axis = "class"
    title = "Distribution of Vegetation Classes"
    labels = {"class": "Class", "count": "Count"}
    fig = px.bar(
        df, x=x_axis, title=title, labels=labels, color_discrete_sequence=["blue"]
    )

    # Customize the layout (optional)
    fig.update_layout(
        xaxis=dict(title="Class"), yaxis=dict(title="Count"), showlegend=False
    )
    return fig

# Function for EDA/Dashboards/Features Used Page
def eda_page():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playwrite+DE+Grund:wght@100..400&display=swap');
        .custom-title {
            font-family: 'Playwrite DE Grund', sans-serif;
            font-size: 2em;
            color: #556B2F; /* color */
            font-weight: bold;
        }
        .custom-header {
            font-family: 'Playwrite DE Grund', sans-serif;
            font-size: 1.5em;
            color: #55a630; /* color */
        }
        .custom-text {
            font-family: 'Playwrite DE Grund', sans-serif;
            font-size: 1em;
            color: #540b0e; /* color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="custom-title">Exploratory Data Analysis (EDA)</p>', unsafe_allow_html=True)
    st.markdown('<p class="custom-header">Feature Distributions and Data Sources</p>', unsafe_allow_html=True)

    st.markdown('<p class="custom-text">Here are the features used in the model along with their distributions:</p>', unsafe_allow_html=True)

    st.markdown("""
    <p class="custom-text">
    Data was collected from various sources such as satellite imagery, geographical surveys, and climate databases.
    Techniques used include remote sensing, GIS analysis, and environmental monitoring.
    </p>
    """, unsafe_allow_html=True)

    # Looker Studio report URL
    report_url = "https://lookerstudio.google.com/embed/reporting/eaab71cb-575f-4f7c-b9ac-97942e43d017/page/r2W2D"

    # Create the iframe HTML
    iframe_code = f"""
    <iframe width="100%" height="1000" src="{report_url}" frameborder="0" style="border:0" allowfullscreen sandbox="allow-storage-access-by-user-activation allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"></iframe>
    """

    # Display the iframe using Streamlit's components.html function
    components.html(iframe_code, height=1000)

    # Read CSVs
    # loading ndvi, ndbi and bu(built-up)
    data = pd.read_csv("dataset/Merged_2014.csv")

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
    with st.expander("Histogram"):
        hist = plot_histogram(hist_data)
        st.plotly_chart(hist)

    # Correlation matrix plot
    with st.expander("Correlation Matrix"):
        cols = ["NDVI", "NDBI", "NDWI", "solar_radiation", "SMI", "LST"]
        fig = plot_correlation(data, cols)
        st.plotly_chart(fig)

    # Scatter plot
    with st.expander("Scatter Plot"):
        scatter_vegetation = plot_scatter(data)
        st.plotly_chart(scatter_vegetation, theme="streamlit", use_container_width=True)

    # Bar chart
    with st.expander("Bar Chart"):
        bar_plot = plot_bar(data)
        st.plotly_chart(bar_plot)

# Run the EDA page function
if __name__ == "__main__":
    eda_page()
