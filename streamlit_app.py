import streamlit as st
import pandas as pd
import numpy as np


data = pd.read_csv("data archive\\data_processed_with_coordinates.csv")

st.title("Boston Housing For Students")
st.write("Finding Home is Easy Now!😉")


distance= ['distance_neu', 'distance_harvard', 'distance_mit', 'distance_bu']
for dis in distance:
    data[dis] = data[dis].str.replace(r'[^\d.]+', '', regex=True).astype(float)

data = data.rename(columns={
    'address': 'House address',
    'bds': 'Bedrooms',
    'distance_neu': 'Distance from Northeastern',
    'distance_mit': 'Distance from MIT',
    'distance_harvard': 'Distance from Harvard',
    'distance_bu': 'Distance from Boston University'
})


st.sidebar.header("Housing Filters")

universities = {
    "Northeastern University": "Distance from Northeastern",
    "Harvard University": "Distance from Harvard",
    "MIT University": "Distance from MIT",
    "Boston University": "Distance from Boston University"
}
university = st.sidebar.selectbox("Choose your University:", list(universities.keys()))

distance_max= st.sidebar.slider("Maximum distance from University (in km):", min_value=1, max_value=20, value=4)

bedrooms = st.sidebar.selectbox("Number of bedrooms:", sorted(data['Bedrooms'].unique()))

min_cost, max_cost = st.sidebar.slider("Budget:", 
                                       min_value=0, 
                                       max_value=20000, 
                                       value=(0, 10000))

distance = universities[university]
filtered_data = data[
    (data[distance] <= distance_max) & 
    (data['Bedrooms'] == bedrooms) & 
    (data['cost'].between(min_cost, max_cost))
]

filtered_data = filtered_data.reset_index(drop=True)

filtered_data['S. No.'] = filtered_data.index + 1

filtered_data = filtered_data[['S. No.', 'House address', 'Bedrooms', 'cost', distance]]


st.subheader("🏡 Here are your matching homes:")

st.write(f"We found {len(filtered_data)} options within {distance_max} km of {university}, "
         f"with {bedrooms} bedrooms and prices between ${min_cost} and ${max_cost}.")

if not filtered_data.empty:
    st.dataframe(filtered_data, use_container_width=True, hide_index=True)
else:
        st.warning(f"Sorry, we could not find any houses matching your criteria")


st.markdown("Don't fall for scams!Good luck💕")

