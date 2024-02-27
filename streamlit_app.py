import streamlit as st
from streamlit_predict import predict
from streamlit_train import clean_data
import pandas as pd
import json 
import streamlit_shadcn_ui as ui

df = pd.read_csv("data/properties.csv")

property_type = df["property_type"].unique().tolist()

def main():


     st.markdown("""
     <div style="text-align:center">
     <h1>Estate price predictor 📈</h1>
     </div>
     """, unsafe_allow_html=True)
     st.text("")

     st.header('Features  👀')

     bedrooms = st.slider('Number of bedrooms', 0, 35, 1)
     living_area = st.slider('What\'s the living area in m²', 0, 500, 1)
     select_prop_type = ui.tabs(options=property_type)
     terrace = st.radio('Does it have a terrace?:', [1, 0])

     inputs = {"nbr_bedrooms": bedrooms, "total_area_sqm": living_area, "fl_terrace": terrace, "property_type": select_prop_type}
     user_data = json.dumps(inputs)

     if st.button('Calculate Reselling Price'):
          prediction = int(predict(user_data))
          formatted_number = f" {prediction:,.0f}"
          st.write(f"The estimated reselling price is: {formatted_number}€")

if __name__ == '__main__':
     main()
