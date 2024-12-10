import streamlit as st
import pandas as pd
import numpy as np
import math
import streamlit.components.v1 as components
import folium
import json
from streamlit_folium import st_folium
import pickle


data = pd.read_csv("data archive\\data_processed_with_coordinates.csv")
with open('uni_coordinates.json', 'r') as file:
    uni_coordinates = json.load(file)

st.title("Boston Housing For Students")
st.write("Finding a Home is Easy Now!😉")


distance= ['distance_neu', 'distance_harvard', 'distance_mit', 'distance_bu']
for dis in distance:
    data[dis] = data[dis].str.replace(r'[^\d.]+', '', regex=True).astype(float)

data = data.rename(columns={
    'address': 'House address',
    'bds': 'Bedrooms',
    'distance_neu': 'Distance from Northeastern',
    'distance_mit': 'Distance from MIT',
    'distance_harvard': 'Distance from Harvard',
    'distance_bu': 'Distance from Boston University',
    'cost': 'Rent'
})

bedroom_list = ["Studio"] + sorted(data['Bedrooms'].unique())[:-1]

st.sidebar.header("Operation Mode")
mode = st.sidebar.selectbox("Choose Operation Mode:", ["Database","Predictive Model"])

if(mode == "Database"):
    st.sidebar.header("Filters")
    universities = {
        "Northeastern University": "Distance from Northeastern",
        "Harvard University": "Distance from Harvard",
        "MIT University": "Distance from MIT",
        "Boston University": "Distance from Boston University"
    }
    university = st.sidebar.selectbox("Choose your University:", list(universities.keys()))

    max_distance = data[universities[university]].max()

    distance_max= st.sidebar.slider("Maximum distance from University (in km):", min_value=1, max_value = math.ceil(max_distance), value=4)

    
    bedrooms = st.sidebar.selectbox("Number of bedrooms:", bedroom_list)

    distance = universities[university]

    filtered_data = data[
        (data[distance] <= distance_max) & 
        (data['Bedrooms'] == bedrooms) 
    ]

    m_cost = filtered_data['Rent'].max()
    mi_cost = filtered_data['Rent'].min()

    min_cost, max_cost = st.sidebar.slider("Budget:", 
                                        value=(mi_cost, m_cost))

    filtered_data = filtered_data[
        (data['Rent'].between(min_cost, max_cost))
    ]

    filtered_data['Rent'] = filtered_data['Rent'].apply(lambda x : "$" + str(x))

    filtered_data = filtered_data.reset_index(drop=True)

    filtered_data['S. No.'] = filtered_data.index + 1

    filtered_data_display = filtered_data[['S. No.', 'House address', 'Bedrooms', 'Rent', distance]]

    st.subheader("🏡 Here are houses matching your requirement:")

    st.write(f"We found {len(filtered_data)} options within {distance_max} km of {university}, "
            f"with {bedrooms} bedrooms and prices between {min_cost} and {max_cost}.")

    if not filtered_data.empty:
        uni_lat = uni_coordinates[university]['latitude']
        uni_lng = uni_coordinates[university]['longitude']
        map_display = folium.Map(location=[uni_lat, uni_lng], zoom_start=14)
        folium.Marker([uni_lat, uni_lng], popup=university, icon=folium.Icon(color='red')).add_to(map_display)
        filtered_data.apply(lambda x : folium.Marker([x['lat'], x['lng']], popup=x['House address']).add_to(map_display), axis = 1)
        map_html = map_display._repr_html_()
        components.html(map_html, height=500)
        st.dataframe(filtered_data_display, use_container_width=True, hide_index=True)
        
    else:
            st.warning(f"Sorry, we could not find any houses matching your criteria")
else:

    st.title("Pick a Coordinate on the Map")

    # Boston coordinates as a starting point
    boston_coords = [42.3601, -71.0589]

    # Create a Folium map centered on Boston
    m = folium.Map(location=boston_coords, zoom_start=13)
    m.add_child(folium.LatLngPopup())
    map = st_folium(m, height=350, width=700)
    with open('model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)
    if map['last_clicked'] != None:
        l = [[i,map['last_clicked']['lat'],map['last_clicked']['lng']] for i in range(0,5)]
        predictions = loaded_model.predict(l)
        l = ["$ " + str(int(i)) for i in predictions]
        d={"No. of bedrooms": bedroom_list[0:5], "Predicred rent": l}
        st.dataframe(pd.DataFrame(d), hide_index=True)
    




footer_html = """    

    <div style="position: fixed; bottom: 5px; background-color: transparent">
    Developed with ❤️ by Reghu, Krishna and Neha
</div>"""

st.markdown(footer_html, unsafe_allow_html=True)