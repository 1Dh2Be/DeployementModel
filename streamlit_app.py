import streamlit as st
from streamlit_train import clean_data
import pandas as pd
import json 
import streamlit_shadcn_ui as ui
import requests

df = pd.read_csv("data/properties.csv")

property_type = df["property_type"].unique().tolist()
province = df["province"].unique().tolist()
province.remove("MISSING")
subproperty_by_type = df.groupby("property_type")["subproperty_type"].unique()
building_state = df["state_building"].unique().tolist()
building_state.remove("MISSING")


def make_api_request(user_input):
    api_url = 'http://127.0.0.1:8000/request' 
    data = user_input
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Failed to make API request'}

def main():


     st.markdown("""
     <div style="text-align:center">
     <h1>Estate price predictor 📈</h1>
     </div>
     """, unsafe_allow_html=True)
     st.text("")

     st.header('Features  👀')

     zip_code, select_province = st.columns(2)
     with zip_code:
          zip_code = st.text_input("Postal code", placeholder="Ex. 1000", max_chars=4, key=int)
     with select_province:
          select_province = st.selectbox("Select the province", options=province, index=None, placeholder="Ex. Brussels")

     bedrooms = st.slider('Number of bedrooms', 0, 35, 1)
     living_area = (st.text_input('What\'s the living area in m²'))


     select_prop_type = ui.tabs(options=property_type, default_value="APARTMENT")
     if select_prop_type == "HOUSE":
          surface_land_sqm = st.text_input("What's the total land area in m²")
          select_subprop_type = st.selectbox("Select Subproperty Type", options=subproperty_by_type["HOUSE"], index=None, placeholder="Select Subproperty...")
     else:
          surface_land_sqm = living_area
          select_subprop_type = st.selectbox("Select Subproperty Type", options=subproperty_by_type["APARTMENT"], index=None, placeholder="Select Subproperty...")
          
     terrace, garden, space = st.columns(3)
     with terrace:
          terrace = st.radio('Does it have a terrace?', ['Yes', 'No'], horizontal=True, index=None)
          if terrace == "Yes":
               terrace_sqm = st.text_input("How big is your terrace (in square meters)?")
          else:
               terrace_sqm = 0

     with garden:
          garden = st.radio('Does it have a garden?', ['Yes', 'No'], horizontal=True, index=None)
          if garden == "Yes":
               garden_sqm = st.text_input("How big is your garden in m²")
          else:
               garden_sqm = 0
     with space:
          st.write("")

     state_building = st.selectbox("What's the building state?", options=building_state, index=None, placeholder="Select building state...")

     energy_consumption = st.text_input("Please specify the energy consumption in kilowatt-hours (kWh).")

     latitude = st.text_input("Give latitude")
     longitude = st.text_input("Give longitude")

     terrace = 1 if terrace == 'Yes' else 0
     garden = 1 if garden == 'Yes' else 0

     inputs = {
          "nbr_bedrooms": bedrooms, 
          "total_area_sqm": living_area, 
          "fl_terrace": terrace, 
          "terrace_sqm": terrace_sqm,
          "fl_garden": garden,
          "garden_sqm": garden_sqm,
          "property_type": select_prop_type,
          "subproperty_type": select_subprop_type,
          "province": select_province,
          "zip_code": zip_code,
          "primary_energy_consumption_sqm": energy_consumption,
          "surface_land_sqm": surface_land_sqm,
          "state_building": state_building,
          "longitude": longitude, 
          "latitude": latitude
          }

     if st.button('Calculate Reselling Price'):
          prediction = make_api_request(inputs)
          predicted_price = prediction['result'][0]
          formatted_number = f" {predicted_price:,.0f}"
          st.write(f"The estimated reselling price is: {formatted_number}€")
          
     # df = pd.read_csv("data/properties.csv")

     # property_type = df["property_type"].unique().tolist()
     # province = df["province"].unique().tolist()
     # province.remove("MISSING")
     # print(province)
     
if __name__ == '__main__':
     main()
