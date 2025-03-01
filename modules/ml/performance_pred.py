import pandas as pd
import streamlit as st
from pathlib import Path
import sqlite3
from . import predictor

def generate_sample_data(model_name, years, months, factories):
    """Generates sample data for multiple months

    Args:
        model_name (str): Name of the model
        years (list): List of years to generate data for
        months (list): List of months to generate data for
        factories (list): List of factories to generate data for
    Returns:
        pd.DataFrame: Generated sample data
    """
    keys = None
    if model_name == 'production_volume_model':
        keys = predictor.keys_prod_volume
        val_dict = predictor.prodvol_mean_dict
    if model_name == 'revenue_model':
        keys = predictor.keys_revenue
        val_dict = predictor.rev_mean_dict
    if model_name == 'profit_margin_model':
        keys = predictor.keys_prof_margin
        val_dict = predictor.prof_margin_mean_dict

    future_data = pd.DataFrame()
    for year in years:
        for month in months:
            for factory in factories:
                temp_data = pd.DataFrame({
                    'month': month,
                    'year': [year],
                    'Factory': [factory]
                })
                for col in keys:
                    if col not in temp_data.columns:
                        temp_data[col] = val_dict[col]

                future_data = pd.concat([future_data, temp_data], ignore_index=True)



    return future_data

def get_vol_prediction_for_6month(target):
    """
    Allows the user to interactively predict targets and analyze parameters.
    """

    input_data = generate_sample_data('production_volume_model', [2025], [1,2,3,4,5,6], [0,1,2,3,4])
    future_predictions = predictor.get_vol_prediction_for_6month(input_data)
    input_data[f'Predicted {target}'] = future_predictions
    

    return input_data

def get_rev_prediction_for_6month(target):
    """
    Allows the user to interactively predict targets and analyze parameters.
    """

    input_data = generate_sample_data('revenue_model', [2025], [1,2,3,4,5,6], [0,1,2,3,4])
    future_predictions = predictor.get_rev_prediction_for_6month(input_data)
    input_data[f'Predicted {target}'] = future_predictions
    
    return input_data

def get_foam_prediction_for_6month(target):
    """
    Allows the user to interactively predict targets and analyze parameters.
    """

    input_data = generate_sample_data('profit_margin_model', [2025], [1,2,3,4,5,6], [0,1,2,3,4])
    future_predictions = predictor.get_foam_prediction_for_6month(input_data)
    input_data[f'Predicted {target}'] = future_predictions
    
    return input_data
