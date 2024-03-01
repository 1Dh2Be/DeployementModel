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
locality_options = df.groupby("region")["locality"].unique().tolist()

belgium_localities = {
    "Antwerp": ["Antwerp", "Mechelen", "Turnhout", "Geel", "Lier", "Mortsel"],
    "East Flanders": ["Gent", "Aalst", "Sint-Niklaas", "Dendermonde", "Oudenaarde", "Ronse"],
    "Flemish Brabant": ["Leuven", "Vilvoorde", "Tienen", "Diest", "Aarschot", "Halle"],
    "Limburg": ["Hasselt", "Genk", "Tongeren", "Sint-Truiden", "Lommel", "Bilzen"],
    "West Flanders": ["Brugge", "Kortrijk", "Ostend", "Roeselare", "Waregem", "Ieper"],
    "Hainaut": ["Mons", "Charleroi", "Tournai", "Mouscron", "La Louvière", "Thuin"],
    "Liège": ["Liège", "Verviers", "Huy", "Seraing", "Herstal", "Waremme"],
    "Luxembourg": ["Arlon", "Marche-en-Famenne", "Bastogne", "Durbuy", "Vielsalm", "La Roche-en-Ardenne"],
    "Namur": ["Namur", "Dinant", "Philippeville", "Rochefort", "Ciney", "Fosses-la-Ville"],
    "Walloon Brabant": ["Wavre", "Nivelles", "Tubize", "Jodoigne", "Genappe", "Ottignies-Louvain-la-Neuve"],
    "Brussels": ["Anderlecht", "Brussels", "Elsene", "Etterbeek", "Evere", "Ganshoren", "Jette", "Koekelberg", "Oudergem", "Schaerbeek", "Sint-Agatha-Berchem", "Sint-Gillis", "Sint-Jans-Molenbeek", "Sint-Joost-ten-Node", "Sint-Lambrechts-Woluwe", "Sint-Pieters-Woluwe", "Uccle", "Vorst", "Watermaal-Bosvoorde"]
}

property_type_mapping = {
    "APARTMENT": {
        "Apartment": "APARTMENT",
        "Duplex": "DUPLEX",
        "Triplex": "TRIPLEX",
        "Penthouse": "PENTHOUSE",
        "Loft": "LOFT",
        "Studio": "FLAT_STUDIO", 
        "Ground Floor": "GROUND_FLOOR"
    },
    "HOUSE": {
        "House": "HOUSE",
        "Villa": "VILLA",
        "Manor House": "MANOR_HOUSE",
        "Country Cottage": "COUNTRY_COTTAGE",
        "Town House": "TOWN_HOUSE",
        "Mansion": "MANSION",
        "Farmhouse": "FARMHOUSE",
        "Bungalow": "BUNGALOW"  
    }
}


mapping_simplified = {
    "Hyper Equipped": "HYPER_EQUIPPED",
    "Installed": "INSTALLED",
    "Semi Equipped": "SEMI_EQUIPPED",
    "Not Installed": "NOT_INSTALLED"
}

building_state_mapping = {
    "Excellent Condition": "AS_NEW",
    "Good": "GOOD",
    "To Renovate": "TO_BE_DONE_UP",
    "Just Renovated": "JUST_RENOVATED",
    "To Restore": "TO_RESTORE"
}

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
     <h1>Fivers price predict-model 🏡</h1>
     </div>
     """, unsafe_allow_html=True)
     st.text("")
     st.divider()
     st.header('Property specifications')

     select_prop_type, blank3, blank4, blank5 = st.columns(4)
     with select_prop_type:
          select_prop_type = st.radio(label="**Select Property Type**", options=["Apartment", "House"], horizontal=True, index=None)       

     with blank3:
          st.write("")
     with blank4:
          st.write("")
     with blank5:
          st.write("")

     if select_prop_type == "House":
          select_subprop_type = st.selectbox("**Subproperty Type**", options=property_type_mapping["HOUSE"], index=None, placeholder="Select House Subproperty...")
     else:
          select_subprop_type = st.selectbox("**Subproperty Type**", options=property_type_mapping["APARTMENT"], index=None, placeholder="Select Apartment Subproperty...")

     select_province, zip_code, locality = st.columns(3)
     with zip_code:
          zip_code = st.text_input("**Postal Code**", placeholder="Ex. 1000", max_chars=4, key=int)
     with select_province:
          select_province = st.selectbox("**Province**", options=province, index=None, placeholder="Ex. Brussels")
     with locality:
          if select_province != None:
               locality = st.selectbox("**Locality**", options=belgium_localities[select_province], index=None, placeholder="Choose a locality")
          else:
               locality = st.selectbox("**Locality**", options=belgium_localities, index=None, placeholder="Ex. Uccle")

     living_area, surface_land_sqm = st.columns(2)
     with living_area:
          living_area = (st.text_input("**Living Area (m²)**"))
     with surface_land_sqm:
          if select_prop_type == "House":
               surface_land_sqm = surface_land_sqm = st.text_input("Total Land Area (m²)")
          else:
               surface_land_sqm = living_area
     
     terrace, garden, blank1, blank2 = st.columns(4)
     with terrace:
          terrace = st.checkbox('**Terrace**')
          if terrace:
               terrace_sqm = st.text_input("**Terrace Area (m²)**")
          else:
               terrace_sqm = 0

     with garden:
          garden = st.checkbox('**Garden**')
          if garden:
               garden_sqm = st.text_input("**Garden Area (m²)**")
          else:
               garden_sqm = 0
     with blank1:
          st.write("")
     with blank2:
          st.write("")

     bedrooms, equiped_kitchen = st.columns(2)
     with bedrooms:
          bedrooms = st.number_input('**Number of Bedrooms**', min_value=0, step=1)
     with equiped_kitchen:
          equiped_kitchen = st.selectbox("**Kitchen Type**", options=mapping_simplified.keys(), index=None, placeholder="Select Kitchen Type...")
     
     state_building, construction_year, energy_consumption = st.columns(3)
     with state_building:
          state_building = st.selectbox("**Building State**", options=building_state_mapping.keys(), index=None, placeholder="Select Building State...")
     with construction_year:
          construction_year =  st.text_input("**Construction Year**", placeholder="Ex. 1990", max_chars=4)
     with energy_consumption:
          energy_consumption = st.text_input("**Energy Consumption (kWh).**")

     st.divider()

     st.write("**Other Amenities Influencing the Price**")
     pool, double_glazing, fl_open_fire, fl_furnished = st.columns(4)

     with pool:
          pool = st.checkbox('**Swimming Pool**')
          if not pool:
               pool = 0
     with double_glazing:
          double_glazing = st.checkbox("**Double Glazing**")
          if not double_glazing:
                    double_glazing = 0
     with fl_open_fire:
          fl_open_fire = st.checkbox("**Open Fire**")
          if not fl_open_fire:
               fl_open_fire = 0

     with fl_furnished:
          fl_furnished = st.checkbox("**Furnished**")
          if not fl_furnished:
               fl_furnished = 0


     nbr_frontages = st.number_input("**Number of Frontages**", 0, 4, 1)

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
          "surface_land_sqm": surface_land_sqm,
          "primary_energy_consumption_sqm": energy_consumption,
          "state_building": building_state_mapping[state_building] if state_building != None else None,
          "fl_double_glazing": double_glazing,
          "fl_swimming_pool": pool,
          "equipped_kitchen": mapping_simplified[equiped_kitchen] if equiped_kitchen != None else None,
          "construction_year": construction_year,
          "nbr_frontages": nbr_frontages,
          "fl_open_fire": fl_open_fire,
          "fl_furnished":fl_furnished,
          "locality": locality
          }

     if st.button('Calculate Price'):
          prediction = make_api_request(inputs)
          predicted_price = prediction['result'][0]
          formatted_number = f" {predicted_price:,.0f}"
          st.write(f"### **Estimated Price: {formatted_number}€**")
     
if __name__ == '__main__':
     main()
