import joblib
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import xgboost as xgb
from sklearn.model_selection import GridSearchCV

def drop_outliers(data):
    """Drops outliers in the data set"""

    # Drop the rows where 'primary_energy_consumption_sqm' is over 1000
    data = data[data['primary_energy_consumption_sqm'] <= 1000]

    # Drop the rows where there are more than 105 bedrooms
    data = data[data['nbr_bedrooms'] <= 50]

    # Delete the rows where there is no province
    data = data[data["province"] != "MISSING"]

    return data

def clean_data(data, imputer=None):
    """Clean the dataset"""

    
    if imputer is None:
        imputer = {}

    # Group by property_type & subproperty_type and take the median before storing it
    mean_sqm_per_category = data.groupby(['property_type', 'subproperty_type'])['total_area_sqm'].median()

    # Fill missing values in 'total_area_sqm' based on median values per category
    data['total_area_sqm'] = data.apply(
        lambda row: mean_sqm_per_category.loc[(row['property_type'], row['subproperty_type'])] 
                     if pd.isna(row['total_area_sqm']) 
                     else row['total_area_sqm'],
        axis=1
    )

    # Save values in dictionary
    imputer['total_area_sqm'] = mean_sqm_per_category

    
    # Group by property_type & province and take the median before storing it
    median_energy_consumption_sqm = data.groupby(['subproperty_type', 'province'])['primary_energy_consumption_sqm'].median()

    # Fill missing values in 'primary_energy_consumption_sqm' based on median values per category
    data['primary_energy_consumption_sqm'] = data.apply(
        lambda row: median_energy_consumption_sqm.loc[(row['subproperty_type'], row['province'])] 
                     if pd.isna(row['primary_energy_consumption_sqm']) 
                     else row['primary_energy_consumption_sqm'],
        axis=1
    )

    # Save values in dictionary
    imputer['primary_energy_consumption_sqm'] = median_energy_consumption_sqm


    # Group by subproperty type & province and store it
    median_sqm_terrace = data.groupby(["subproperty_type", "province"])["terrace_sqm"].median()

    # Fill missing values in 'ter' based on median values per category
    data["terrace_sqm"] = data.apply(
        lambda row: median_sqm_terrace.loc[(row['subproperty_type'], row['province'])] 
                     if pd.isna(row['terrace_sqm']) 
                     else row['terrace_sqm'],
        axis=1
    )

    # Save values in dictionary
    imputer["terrace_sqm"] = median_sqm_terrace


    median_sqm_garden = data.groupby(["subproperty_type", "province"])["garden_sqm"].mean()

    data["garden_sqm"] = data.apply(
        lambda row: median_sqm_garden.loc[(row['subproperty_type'], row['province'])] 
                     if pd.isna(row['garden_sqm']) 
                     else row['garden_sqm'],
        axis=1
    )

    # Save values in dictionary
    imputer["garden_sqm"] = median_sqm_garden

    return data, imputer

def train():
    """Trains a linear regression model on the full dataset and stores output."""
    # Load the data
    data = pd.read_csv("src/data/properties.csv")

    # Drop outliers
    data = drop_outliers(data)

    # Define features to use
    num_features = ["total_area_sqm", "nbr_bedrooms",
                    "primary_energy_consumption_sqm",
                    "terrace_sqm","construction_year",
                    "garden_sqm", "surface_land_sqm", 
                    "nbr_frontages"]
    
    fl_features = ["fl_terrace", "fl_garden", "fl_furnished", 
                   "fl_swimming_pool", "fl_double_glazing",
                   "fl_open_fire"]

    cat_features = ["subproperty_type", "province", "state_building",
                    "property_type", "locality", "zip_code"]

    # Split the data into features and target
    X = data[num_features + fl_features + cat_features]
    y = data["price"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=505
    )

    # Clean the training data
    X_train, imputer = clean_data(X_train)

    # Impute missing values in the testing data based on information from the training data
    X_test, _ = clean_data(X_test, imputer)


    # Convert categorical columns with one-hot encoding using OneHotEncoder
    enc = OneHotEncoder(handle_unknown="ignore")
    enc.fit(X_train[cat_features])
    X_train_cat = enc.transform(X_train[cat_features]).toarray()
    X_test_cat = enc.transform(X_test[cat_features]).toarray()

    # Combine the numerical and one-hot encoded categorical columns
    X_train = pd.concat(
        [
            X_train[num_features + fl_features].reset_index(drop=True),
            pd.DataFrame(X_train_cat, columns=enc.get_feature_names_out()),
        ],
        axis=1,
    )

    X_test = pd.concat(
        [
            X_test[num_features + fl_features].reset_index(drop=True),
            pd.DataFrame(X_test_cat, columns=enc.get_feature_names_out()),
        ],
        axis=1,
    )

    # Define the parameter grid
    param_grid = {
        'n_estimators': [650],
        'max_depth': [7],
        'learning_rate': [0.1],
        'lambda': [0.5]
    }

    # Initialize the XGBoost regressor
    model = xgb.XGBRegressor(objective='reg:squarederror', random_state=505)

    # Initialize the GridSearchCV object
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='r2')

    # Fit the GridSearchCV object to the data
    grid_search.fit(X_train, y_train)

    # Get the best parameters
    best_params = grid_search.best_params_
    print(best_params)

    # Train the model with the best parameters
    model = xgb.XGBRegressor(objective='reg:squarederror', random_state=505, **best_params)
    model.fit(X_train, y_train)

    # Evaluate the model
    train_score = r2_score(y_train, model.predict(X_train))
    test_score = r2_score(y_test, model.predict(X_test))
    print(f"\nTrain R² score: {train_score}", end="")
    print(f" Test R² score: {test_score}")

    # Add the 20% left of the dataset 
    model.fit(pd.concat([X_train, X_test]), pd.concat([y_train, y_test]))
    final_R2_score = r2_score(pd.concat([y_train, y_test]), model.predict(pd.concat([X_train, X_test])))
    print(f"final R² score: {final_R2_score}", end="")

    artifacts = {
        "features": {
            "num_features": num_features,
            "fl_features": fl_features,
            "cat_features": cat_features,
        },
        "enc": enc,
        "model": model,
    }
    joblib.dump(artifacts, "src/artifacts.joblib")

if __name__ == "__main__":
    train()

    # directory = /Users/MimounB/Desktop/Projects/DeployementModel