import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('data/all_services_binarized.csv')
    gdf = gpd.read_file('data/va_county/va.shp')
    return df, gdf

df, gdf = load_data()

# Merge the dataframes
merged = gdf.merge(df, left_on='NAME', right_on='County', how='left')

# Create the app
st.title('Virginia Services Dashboard')

# Dropdown for service selection
service = st.selectbox(
    'Select a service:',
    ('School Services', 'Adult Services', 'Behavioral Health')
)

# Define the custom color list
custom_colors = ['#007bff', '#FFC300', '#000080']

fig = px.choropleth_mapbox(merged, 
                           geojson=merged.geometry, 
                           locations=merged.index, 
                           color=service,
                           color_discrete_map=custom_colors,
                           mapbox_style="carto-positron",
                           zoom=6, 
                           center = {"lat": 37.5, "lon": -78.5},
                           opacity=0.5,
                           labels={service:'Available'}
                          )

fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    coloraxis_showscale=False  # or showlegend=False for discrete color maps
)

# Display only the map, without the data table
fig.show(config={'displayModeBar': False, 'staticPlot': False})

# Show the map
st.plotly_chart(fig)