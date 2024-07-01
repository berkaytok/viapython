import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

# Set page config to use full width
st.set_page_config(layout="wide")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("data/all_services_binarized.csv")
    gdf = gpd.read_file("data/va_county/va.shp")
    return df, gdf

df, gdf = load_data()

# Ensure service columns are integers
service_columns = ["School Services", "Adult Services", "Behavioral Health"]
for col in service_columns:
    df[col] = df[col].astype(int)

# Merge the dataframes
merged = gdf.merge(df, left_on="NAME", right_on="County", how="left")

# Create the app
st.title("Virginia Services Dashboard")

# Dropdown for service selection
service = st.selectbox(
    "Select a service:", service_columns
)

# Define the custom color list
custom_colors = ["#14467C", "#72BF44", "#00AFAD"]

# Create a custom hover text and handle NaN values
def hover_text(row):
    if pd.isna(row[service]):
        return f"County: {row['NAME']}<br>{service}: No data"
    else:
        return f"County: {row['NAME']}<br>{service}: {'Yes' if row[service] == 1 else 'No'}"

merged['hover_text'] = merged.apply(hover_text, axis=1)

# Create a new column for coloring
merged['color_category'] = merged[service].map({0: 'No', 1: 'Yes'}).fillna('No data')

fig = px.choropleth_mapbox(
    merged,
    geojson=merged.geometry,
    locations=merged.index,
    color='color_category',
    color_discrete_map={'No': custom_colors[0], 'Yes': custom_colors[1], 'No data': custom_colors[2]},
    mapbox_style="carto-positron",
    zoom=6,
    center={"lat": 37.5, "lon": -78.5},
    opacity=0.5,
    labels={'color_category': service},
    hover_data={'hover_text': True},
    custom_data=['hover_text']
)

fig.update_traces(
    hovertemplate='%{customdata[0]}<extra></extra>'
)

fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=800,  # Adjust this value to fit your screen
)

# Show the map
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})