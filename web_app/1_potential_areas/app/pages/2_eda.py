import streamlit as st
import pandas as pd
import json
import geopandas as gpd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pathlib import Path

# Root Path
root_path = Path(__file__).parent.parent.parent.parent.parent


# Function for EDA/Dashboards/Features Used Page
def eda_page():
    app_path = 'web_app/1_potential_areas/app'
    pages_path = root_path.joinpath(app_path).joinpath('pages')
    
    col1, col2, col3, col4 = st.columns([1,1,3,1], gap='medium')
    with col1:
        st.page_link(str(pages_path.joinpath("1_home.py")), label="Home", icon="🏠")
    with col2:
        st.page_link(str(pages_path.joinpath("2_eda.py")), label="EDA", icon="📶")
    with col3:
        st.page_link(str(pages_path.joinpath("3_prediction.py")), label="Find Suitable Area for Uraban Farming", icon="🤖")
    with col4:
        st.page_link(str(pages_path.joinpath("4_contact.py")), label="Contact Us", icon="📧")

    # st.set_page_config(page_icon=':bar_chart:')
    st.title("Exploratory Data Analysis")
    st.header("Feature Distributions and Data Sources")

    st.write("Here are the features used in the model along with their distributions:")

    # Data to simulate EDA

    # Display distributions of each feature
    
    st.write("""
    Data was collected from various sources such as satellite imagery, geographical surveys, and climate databases.
    Techniques used include remote sensing, GIS analysis, and environmental monitoring.
    """)

eda_page()


data_dir = root_path.joinpath('data')
data_path = '1_potential_areas/processed/Opeyemi'

@st.cache_data
def read_csv(filename, index_col=None):
    df = pd.read_csv(data_dir.joinpath(data_path).joinpath(filename),index_col=index_col, engine='pyarrow')
    return df


# Function to extract coordinates
def extract_coordinates(point):
    point_dict = json.loads(point)['coordinates']
    longitude = point_dict[0]
    latitude = point_dict[1]
    return longitude, latitude

# Convert pandas dataframes to geopandas geodataframes and perform a spatial join.
def convert_and_join(df1, df2, max_distance=0.01):
    # Convert pandas dataframes to geopandas geodataframes
    gdf1 = gpd.GeoDataFrame(df1, geometry=gpd.points_from_xy(df1.longitude, df1.latitude))
    gdf2 = gpd.GeoDataFrame(df2, geometry=gpd.points_from_xy(df2.longitude, df2.latitude))

    # Perform the spatial join
    merged_gdf = gpd.sjoin_nearest(gdf1, gdf2, how='inner', max_distance=max_distance)

    # Drop specific columns and convert back to pandas DataFrame
    cols_to_drop = ['geometry', 'index_right', 'longitude_right', 'latitude_right']
    merged_gdf = pd.DataFrame(merged_gdf.drop(columns=cols_to_drop, errors='ignore'))

    return merged_gdf


# Function to classify vegetation based on NDVI value
def classify_vegetation(ndvi):
    if ndvi < 0.1:
        return 'Bare Soil/ Built-up Areas'
    elif 0.1 <= ndvi < 0.2:
        return 'Sparse Vegetation'
    elif 0.2 <= ndvi < 0.5:
        return 'Moderate Vegetation'
    elif ndvi >= 0.5:
        return 'Dense Vegetation'
    else:
        return 'null'


@st.cache_data
def plot_histogram(data):
    # Creating a subplot figure with Plotly
    fig = make_subplots(rows=3, cols=3, subplot_titles=[title for _, title in data])

    # Adding histograms to the subplots
    for i, (values, title) in enumerate(data, 1):
        row = (i - 1) // 3 + 1
        col = (i - 1) % 3 + 1
        fig.add_trace(
            go.Histogram(x=values, name=title, histnorm='density', showlegend=False),
            row=row, col=col
        )

    # Update layout
    fig.update_layout(height=800, width=1000, title_text="Distribution Plots", showlegend=False)
    return fig


# Compute the correlation matrix and plot
@st.cache_data
def plot_correlation():
    cols = ['NDVI', 'NDBI', 'NDWI', 'BU', 'Solar(kWh/m2)', 'Air_temperature', 'precipitation', 'Soil_temperature', 'Soil_moisture']
    correlation_matrix = vegsun_climatesoil[cols].corr()

    # Create a Plotly heatmap
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1,
        colorbar=dict(title="Correlation")
    ))

    # Update layout
    fig.update_layout(
        title='Correlation Matrix of Vegetation Indices',
        width=800,
        height=700
    )
    return fig

# Scatter plot of geographical data
@st.cache_data
def plot_scatter():
    fig = px.scatter(vegsun_climatesoil, x='longitude', y='latitude', color='class',
                    title='Geographical Distribution of Vegetation Classes',
                    labels={'longitude': 'Longitude', 'latitude': 'Latitude', 'class': 'Vegetation Class'},
                    color_discrete_map={'Class1': 'blue', 'Class2': 'green', 'Class3': 'red'})

    # Customize the layout
    fig.update_layout(
        legend=dict(title='Vegetation Class'),
        xaxis=dict(title='Longitude'),
        yaxis=dict(title='Latitude'),
        hovermode='closest'
    )
    return fig


# Bar chart
@st.cache_data
def plot_bar():
    fig = px.bar(vegsun_climatesoil, x='class', 
                title='Distribution of Vegetation Classes',
                labels={'class': 'Class', 'count': 'Count'},
                color_discrete_sequence=['blue'])

    # Customize the layout (optional)
    fig.update_layout(
        xaxis=dict(title='Class'),
        yaxis=dict(title='Count'),
        showlegend=False
    )
    return fig



# Read CSVs
#loading ndvi, ndbi and bu(built-up)
built_up = read_csv('NDBI_NDVI_BUILT_new.csv')
ndwi_index = read_csv('NDWI.csv')
#loading the sunlight data
sunlight = read_csv('Solar_Exposure_Zone9.csv')
soil_climate = read_csv('climate_soil.csv', index_col=0)
# Apply the function to the 'point' column
ndwi_index[['longitude', 'latitude']] = ndwi_index['.geo'].apply(lambda x: pd.Series(extract_coordinates(x)))
ndwi = ndwi_index[['longitude', 'latitude', 'NDWI']]


vegetation = convert_and_join(built_up, ndwi)
vegetation.rename(columns = {'longitude_left':'longitude', 'latitude_left':'latitude'}, inplace = True)
vegetation=vegetation[['longitude', 'latitude', 'NDVI', 'NDBI', 'BU', 'NDWI']]

veg_sun =convert_and_join(vegetation, sunlight)
veg_sun.rename(columns=({'longitude_left': 'longitude', 'latitude_left': 'latitude'}), inplace= True)

vegsun_climatesoil = convert_and_join(veg_sun, soil_climate)
vegsun_climatesoil.drop(columns=('Zone'), inplace= True)
vegsun_climatesoil.rename(columns=({'longitude_left': 'longitude', 'latitude_left': 'latitude','GHI (kWh/m2)':'Solar(kWh/m2)' }), inplace= True)
    
# Apply the classification function to the NDVI column and create a class column
vegsun_climatesoil['class'] = vegsun_climatesoil['NDVI'].apply(classify_vegetation)


data = [
    (vegsun_climatesoil['NDVI'], 'NDVI Distribution'),
    (vegsun_climatesoil['NDBI'], 'NDBI Distribution'),
    (vegsun_climatesoil['NDWI'], 'Water Distribution'),
    (vegsun_climatesoil['BU'], 'BU Distribution'),
    (vegsun_climatesoil['Solar(kWh/m2)'], 'Sunlight Distribution'),
    (vegsun_climatesoil['Air_temperature'], 'Air Temperature'),
    (vegsun_climatesoil['precipitation'], 'Precipitation'),
    (vegsun_climatesoil['Soil_temperature'], 'Soil Temperature'),
    (vegsun_climatesoil['Soil_moisture'], 'Soil Moisture')
]

# Histogram
with st.expander("Histogram"):
    hist = plot_histogram(data)
    st.plotly_chart(hist)

# Correlation matrix plot
with st.expander("Correlation Matrix"):
    fig = plot_correlation()
    st.plotly_chart(fig)

# Scatter plot
with st.expander("Scatter Plot"):
    scatter_vegetation = plot_scatter()
    st.plotly_chart(scatter_vegetation, theme="streamlit", use_container_width=True)

# Bar chart
with st.expander("Bar Chart"):
    bar_plot = plot_bar()
    st.plotly_chart(bar_plot)
