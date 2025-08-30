import json
import pickle
import numpy as np
import pandas as pd
import os

__data_columns = None
__model = None
__scaler = None

# Numeric columns that require scaling
__numeric_cols = ["total_sqft", "bath", "bhk", "built_year", "property_age"]

# Build absolute path to artifacts folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_PATH = os.path.join(BASE_DIR, "artifacts")


def load_saved_artifacts():
    """
    Load model, column metadata, and scaler from artifacts folder.
    """
    global __data_columns
    global __model
    global __scaler

    print("loading saved artifacts...start")
    print(f"Artifacts path: {ARTIFACTS_PATH}")  # Debug for Render

    try:
        with open(os.path.join(ARTIFACTS_PATH, "columns.json"), "r") as f:
            __data_columns = json.load(f)["data_columns"]

        if __model is None:
            with open(os.path.join(ARTIFACTS_PATH, "banglore_home_prices_model.pickle"), "rb") as f:
                __model = pickle.load(f)

        if __scaler is None:
            with open(os.path.join(ARTIFACTS_PATH, "std_scaler.pickle"), "rb") as f:
                __scaler = pickle.load(f)

        print(f"Loaded {len(__data_columns)} columns and scaler successfully")
        print("loading saved artifacts...done")
    except Exception as e:
        print(f"ERROR loading artifacts: {e}")
        raise


def set_one_hot(x, prefix, value, data_columns):
    """
    Helper to set one-hot encoded feature in vector x.
    Converts value to lowercase and trims spaces for matching.
    """
    if value:
        col_name = f"{prefix}_{value.strip().lower()}"
        if col_name in data_columns:
            x[data_columns.index(col_name)] = 1


def get_estimated_price(total_sqft, bath, bhk, built_year, property_age,
                        area_type=None, availability=None, location=None,
                        nearby_metro=None, age_segment=None):
    """
    Predict house price in lakhs for given features.
    """
    if __data_columns is None or __model is None or __scaler is None:
        load_saved_artifacts()

    # Create zero vector
    x = np.zeros(len(__data_columns))

    # ---- scale numeric features ----
    numeric_df = pd.DataFrame(
        [[total_sqft, bath, bhk, built_year, property_age]],
        columns=__numeric_cols
    )
    scaled_numeric = __scaler.transform(numeric_df)[0]

    for i, col in enumerate(__numeric_cols):
        if col in __data_columns:
            x[__data_columns.index(col)] = scaled_numeric[i]

    # ---- one-hot categorical features (all lowercased) ----
    set_one_hot(x, "area_type", area_type, __data_columns)
    set_one_hot(x, "availability", availability, __data_columns)
    set_one_hot(x, "location", location, __data_columns)
    set_one_hot(x, "nearby_metro", nearby_metro, __data_columns)
    set_one_hot(x, "age_segment", age_segment, __data_columns)

    # Predict
    X_df = pd.DataFrame([x], columns=__data_columns)
    predicted_price = __model.predict(X_df)[0]
    return round(predicted_price, 2)


def get_location_names():
    """
    Get all available location names
    """
    global __data_columns
    if __data_columns is None:  # Ensure artifacts are loaded
        load_saved_artifacts()
    return [col.replace("location_", "") for col in __data_columns if col.startswith("location_")]


def get_data_columns():
    """
    Get full list of column names
    """
    if __data_columns is None:  # Ensure artifacts are loaded
        load_saved_artifacts()
    return __data_columns


if __name__ == "__main__":
    # Test script mode
    load_saved_artifacts()
    print(get_data_columns()[:20])  # show first 20 columns

    price = get_estimated_price(
        total_sqft=1000,
        bath=2,
        bhk=2,
        built_year=2015,
        property_age=8,
        area_type="built-up  area",
        availability="ready to move",
        location="1st phase jp nagar",
        nearby_metro="yes",
        age_segment="mid"
    )

    print(f"Predicted price: {price} lakhs")
