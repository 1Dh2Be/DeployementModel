import joblib
from streamlit_train import clean_data
import json
import pandas as pd 

def checker(data, features):

    data_dict = {}
    for feature in features:
        if feature in data:
            
            data_dict[feature] = data[feature]
    
    # Create a DataFrame from the data dictionary
    df = pd.DataFrame([data_dict])

    return df
    

def predict(input_dataset):
    """Predicts house prices from 'input_dataset', stores it to 'output_dataset'."""
    ### -------- DO NOT TOUCH THE FOLLOWING LINES -------- ###
    # Load the data
    data = json.loads(input_dataset)
    ### -------------------------------------------------- ###

    # Load the model artifacts using joblib
    artifacts = joblib.load("models/artifacts1.joblib")

    # Unpack the artifacts
    num_features = artifacts["features"]["num_features"]
    fl_features = artifacts["features"]["fl_features"]
    cat_features = artifacts["features"]["cat_features"]
    enc = artifacts["enc"]
    model = artifacts["model"]

    all_features = num_features + fl_features + cat_features

    # Extract the used data
    filtered_data = checker(data, all_features)

    # test = [cat_feature for cat_feature in filtered_data if cat_feature in cat_features]
    # tri = filtered_data[test]

    # # Apply encoder on categorical features
    data_cat = enc.transform(filtered_data[[cat_feature for cat_feature in filtered_data if cat_feature in cat_features]]).toarray()
    

    # Combine the numerical and one-hot encoded categorical columns
    data = pd.concat(
            [
                filtered_data[num_features + fl_features].reset_index(drop=True),
                pd.DataFrame(data_cat, columns=enc.get_feature_names_out()),
            ],
            axis=1,
        )

    # Make predictions
    predictions = model.predict(data)

    return predictions
        
# # Load the model artifacts using joblib
# artifacts = joblib.load("models/artifacts.joblib")

# # Unpack the artifacts
# num_features = artifacts["features"]["num_features"]
# fl_features = artifacts["features"]["fl_features"]
# cat_features = artifacts["features"]["cat_features"]
# enc = artifacts["enc"]
# model = artifacts["model"]


# inputs = {"nbr_bedrooms": 9, "total_area_sqm": 6, "property_type": "House"}

# for feature in num_features:
#     for k, v in inputs.items():
#         if k == feature:
#             print(v)