from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import webbrowser
import folium

# Load the CSV file into a DataFrame
df = pd.read_csv("locations.csv")

# Drop rows with NaN values in latitude or longitude
df = df.dropna(subset=['Latitude', 'Longitude'])

# Function to generate Google Maps link for all locations
def generate_gmaps_link(data):
    base_url = "https://www.google.com/maps/dir/"
    coordinates = []
    for index, row in data.iterrows():
        coordinates.append(f"{row['Latitude']},{row['Longitude']}")
    coordinates_str = "/".join(coordinates)
    gmaps_link = base_url + coordinates_str
    return gmaps_link

# Function to display individual Google Maps link for each location
def display_individual_links(data):
    st.header("Coordenadas de cada banheiro:")
    for index, row in data.iterrows():
        st.subheader(f"{row['Place']}")
        st.write('' if pd.isna(row['Description']) else row['Description'])
        gmaps_link = f"https://www.google.com/maps/search/?api=1&query={row['Latitude']},{row['Longitude']}"
        st.markdown(f"[Abrir no Google Maps]({gmaps_link})")

# Function to create a map with pins for all locations
def display_map_with_pins(data):
    m = folium.Map(location=[-22.9068, -43.1729], zoom_start=13)
    for index, row in data.iterrows():
        try:
            lat, lon = float(row['Latitude']), float(row['Longitude'])
            folium.Marker([lat, lon], popup=row['Place']).add_to(m)
        except ValueError:
            print(f"Invalid coordinates for row {index + 1}: {row['Latitude']}, {row['Longitude']}")
    folium_static(m)

# Function to display a button to open all locations in Google Maps
def display_open_all_button(data):
    if st.button("Abrir no Google Maps"):
        gmaps_link = generate_gmaps_link(data)
        webbrowser.open(gmaps_link)
        # st.markdown(f"[Open All Locations in Google Maps]({gmaps_link})")

st.title("Banheiros - Carnaval Rio 2024")
st.markdown("Mapeamento: [Instagram Cidade Pirata](https://www.instagram.com/p/C3BoEmWJykg/?igsh=cnAxMW5wdGx5bGQw)")
st.markdown("Desenvolvimento: [Daniel N. Rocha](https://www.linkedin.com/in/danielnrocha)")
# Call the functions to display the options
display_open_all_button(df)
display_map_with_pins(df)
display_individual_links(df)
