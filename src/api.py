from fastapi import FastAPI
from pydantic import BaseModel
from predict import predict

app = FastAPI()

class InputData(BaseModel):
    nbr_bedrooms: int
    total_area_sqm: int
    fl_terrace: int
    terrace_sqm: int
    fl_garden: int
    garden_sqm: int
    property_type: object
    subproperty_type: object
    province: object
    zip_code: int
    primary_energy_consumption_sqm: int
    surface_land_sqm: int
    state_building: object
    fl_double_glazing: int
    fl_swimming_pool: int
    construction_year: int
    equipped_kitchen: object
    nbr_frontages: int
    fl_furnished: int
    fl_open_fire: int
    locality: object

@app.get('/')
def greet_people():
    return "Hello there, this is the root of the api :)"

@app.post("/request")
def process_request(input_data:InputData) -> dict:
    value = predict(input_data)
    return {"result": value}