
import pandas as pd
import streamlit as st
df = pd.read_csv("data/properties.csv")

locality_options = df.groupby("province")["locality"].unique().tolist()

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
    "Brussels-Capital Region": ["Anderlecht", "Brussels", "Elsene", "Etterbeek", "Evere", "Ganshoren", "Jette", "Koekelberg", "Oudergem", "Schaerbeek", "Sint-Agatha-Berchem", "Sint-Gillis", "Sint-Jans-Molenbeek", "Sint-Joost-ten-Node", "Sint-Lambrechts-Woluwe", "Sint-Pieters-Woluwe", "Uccle", "Vorst", "Watermaal-Bosvoorde"]
}

building_state_mapping = {
    "Excellent condition": "AS_NEW",
    "Freshly renovated": "GOOD",
    "Good": "TO_RENOVATE",
    "To renovate": "TO_BE_DONE_UP",
    "To refresh": "JUST_RENOVATED",
    "To restore": "TO_RESTORE"
}

house = df.groupby('property_type')["subproperty_type"].unique().tolist()


x = "Excellent condition"

test = building_state_mapping[x]

property_type = df["property_type"].unique().tolist()

# select_prop_type, blank3, blank4, blank5 = st.columns(4)
# with select_prop_type:

# Create the tabbed interface

# tab1, tab2 = st.tabs(tabs=property_type)
# with tab1:
#     cat = 1
#     st.write(cat)
# with tab2:
#     horse = 2
#     st.write(horse)

  
select_prop_type = st.tabs(tabs=["HOUSE", "APARTMENT"])

st.write(select_prop_type["HOUSE"])