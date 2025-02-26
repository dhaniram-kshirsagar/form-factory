import pandas as pd
import streamlit as st
from pathlib import Path
import sqlite3
from . import predictor

db_path = Path(__file__).parent.parent/'data/Factory_Data.db'
table_name = "Sample_Data_5000_v1"


def load_data(db_path, table_name):
    """
    Connects to the SQLite database and loads the data from the specified table.
    """
    try:
        conn = sqlite3.connect(db_path)
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql(query, conn)
        conn.close()
        return data
    except sqlite3.OperationalError as e:
        return pd.DataFrame({"Message": [f"Error: {e}. Please ensure the table '{table_name}' exists in the database."]})

def generate_sample_data(model_name, years, months, factories, locations):
    """Generates sample data for multiple months and locations.

    Args:
        model_name (str): Name of the model
        years (list): List of years to generate data for
        months (list): List of months to generate data for
        factories (list): List of factories to generate data for
        locations (list): List of locations to generate data for

    Returns:
        pd.DataFrame: Generated sample data
    """
    future_data = pd.DataFrame()
    for year in years:
        for month in months:
            for factory in factories:
                for location in locations:
                    temp_data = pd.DataFrame({
                        'month': month,
                        'year': [year],
                        'Factory': [factory],
                        'Location': [location]
                    })
                    for col in predictor.keys_revenue:
                        if col not in temp_data.columns:
                            temp_data[col] = predictor.rev_mean_dict[col]

                    future_data = pd.concat([future_data, temp_data], ignore_index=True)



    return future_data

# @st.cache_data
# def get_vol_prediction_for_6month(target):
#     """
#     Allows the user to interactively predict targets and analyze parameters.
#     """

#     output_df = pd.DataFrame()
#     data = load_data(db_path, table_name)

#     if data.empty:
#         return pd.DataFrame({"Message": ["Error: Data could not be loaded or is empty."]})

#     if target not in data.columns:
#         output_df = pd.concat([output_df, pd.DataFrame({"Message": [f"Error: '{target}' column is missing from the data."]})])
#         return output_df

#     input_data = generate_sample_data('revenue_model', [2025], [1,2,3,4,5,6], [0,1,2,3,4], [0,1,2,3,4])
#     future_predictions = predictor.get_vol_prediction_for_6month(input_data)
#     input_data[f'Predicted {target}'] = future_predictions
    

#     return input_data

@st.cache_data
def get_rev_prediction_for_6month(target):
    """
    Allows the user to interactively predict targets and analyze parameters.
    """
    output_df = pd.DataFrame()
    # data = load_data(db_path, table_name)

    # if data.empty:
    #     return pd.DataFrame({"Message": ["Error: Data could not be loaded or is empty."]})

    # if target not in data.columns:
    #     output_df = pd.concat([output_df, pd.DataFrame({"Message": [f"Error: '{target}' column is missing from the data."]})])
    #     return output_df

    # data, preprocess_output = preprocess_data(data)
    #output_df = pd.concat([output_df, preprocess_output])

    # independent_variables = data.drop(columns=[target], errors='ignore').columns

    input_data = generate_sample_data('revenue_model', [2025], [1,2,3,4,5,6], [0,1,2,3,4], [0,1,2,3,4])
    future_predictions = predictor.get_rev_prediction_for_6month(input_data)
    input_data[f'Predicted {target}'] = future_predictions
    
    return input_data

# @st.cache_data
# def get_foam_prediction_for_6month(target):
#     """
#     Allows the user to interactively predict targets and analyze parameters.
#     """
#     output_df = pd.DataFrame()
#     data = load_data(db_path, table_name)

#     if data.empty:
#         return pd.DataFrame({"Message": ["Error: Data could not be loaded or is empty."]})

#     if target not in data.columns:
#         output_df = pd.concat([output_df, pd.DataFrame({"Message": [f"Error: '{target}' column is missing from the data."]})])
#         return output_df

#     data, preprocess_output = preprocess_data(data)
#     #output_df = pd.concat([output_df, preprocess_output])

#     independent_variables = data.drop(columns=[target], errors='ignore').columns

#     input_data = get_input_data(data, independent_variables, target)
#     future_predictions = predictor.get_foam_prediction_for_6month(input_data)
#     input_data[f'Predicted {target}'] = future_predictions
    
#     return input_data
