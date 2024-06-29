import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
from streamlit_folium import folium_static

# Set page title
st.set_page_config(page_title="Virginia Services Availability Map", layout="wide")

# Add a title
st.title("Virginia Services Availability Map")


# Read the shapefile
@st.cache_data
def load_shapefile():
    return gpd.read_file("data/va_county/va.shp")


shp = load_shapefile()
shp_geojson = shp.to_json()


# Read the CSV file
@st.cache_data
def load_csv():
    return pd.read_csv("data/va_services.csv")


va_data = load_csv()

# Create a Folium map object
m = folium.Map(location=[37.5, -78.5], zoom_start=7)

# Add county polygons to the map
style_function = lambda feature: {
    "fillColor": "green",
    "color": "black",
    "weight": 0.5,
    "fillOpacity": 0.5,
}
folium.GeoJson(
    shp_geojson, name="Virginia Counties", style_function=style_function
).add_to(m)

# Dictionary to map service abbreviations to full names
service_names = {
    "ss": "Support Services",
    "as": "Accommodation Services",
    "bhs": "Behavioral Health Services",
}

# Add markers for the cities with availability information
for _, row in va_data.iterrows():
    popup_content = f"""
    <strong>{row['city'].capitalize()}</strong><br>
    Availability:<br>
    """
    for service in ["ss", "as", "bhs"]:
        status = "Available" if row[service] == 1 else "Not Available"
        popup_content += f"{service_names[service]}: {status}<br>"

    # Hardcoded coordinates for each city
    coordinates = {
        "charlottesville": [38.0293, -78.4767],
        "roanoke": [37.2710, -79.9414],
        "lynchburg": [37.4138, -79.1422],
        "lexington": [37.7840, -79.4428],
    }

    folium.Marker(
        location=coordinates[row["city"]],
        popup=folium.Popup(popup_content, max_width=300),
        tooltip=row["city"].capitalize(),
    ).add_to(m)

# Display the map in Streamlit
folium_static(m)

# Add a footer
st.markdown("---")
st.markdown("Data source: Virginia Services Availability Dataset")