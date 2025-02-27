import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib

# Preprocessing configuration
CATEGORICAL_FEATURES = [
    'Factory', 'Location', 'Product Category', 
    'Machine Type', 'Supplier'
]
NUMERICAL_FEATURES = [
    'month', 'year', 'Cycle Time (minutes)',
    'Waste Generated (kg)', 'Production Volume (units)',
    'Water Usage (liters)', 'Machine Utilization (%)',
    'Machine Age (years)', 'Operator Experience (years)'
]

def encode_revenue_data(df):
    """Encode and preprocess revenue prediction features"""
    # Create copies to avoid modifying original data
    df = df.copy()
    
    # Handle categorical features
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    encoded_cats = encoder.fit_transform(df[CATEGORICAL_FEATURES])
    encoded_cats_df = pd.DataFrame(
        encoded_cats,
        columns=encoder.get_feature_names_out(CATEGORICAL_FEATURES)
    )
    
    # Scale numerical features
    scaler = StandardScaler()
    scaled_nums = scaler.fit_transform(df[NUMERICAL_FEATURES])
    scaled_nums_df = pd.DataFrame(
        scaled_nums,
        columns=NUMERICAL_FEATURES
    )
    
    # Combine processed features
    processed_df = pd.concat([encoded_cats_df, scaled_nums_df], axis=1)
    
    # Save preprocessing objects for future use
    joblib.dump(encoder, 'revenue_encoder.pkl')
    joblib.dump(scaler, 'revenue_scaler.pkl')
    
    return processed_df

def clean_revenue_data(df):
    """Clean and validate revenue prediction input data"""
    # Validate required columns
    required_columns = CATEGORICAL_FEATURES + NUMERICAL_FEATURES
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Missing required columns. Expected: {required_columns}")
    
    # Fill missing values
    df = df.fillna({
        'month': 1,
        'year': 2025,
        'Cycle Time (minutes)': 20.0,
        'Production Volume (units)': 300.0,
        'Machine Utilization (%)': 75.0
    })
    
    # Enforce data types
    df = df.astype({
        'month': 'int',
        'year': 'int',
        'Cycle Time (minutes)': 'float',
        'Waste Generated (kg)': 'float',
        'Production Volume (units)': 'float',
        'Water Usage (liters)': 'float',
        'Machine Utilization (%)': 'float',
        'Machine Age (years)': 'float',
        'Operator Experience (years)': 'float'
    })
    
    return df
