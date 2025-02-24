import pandas as pd
import joblib
from pathlib import Path

# Define feature columns
FEATURE_COLUMNS = [
    "Year", "Month", "Day", "Factory"
]

# Define mean values for sample input data
SAMPLE_DATA = {
    "Year": 2025,
    "Month": 1,
    "Day": 2,
    "Factory": 2
}

# Load the trained production volume model
MODEL_FILE = "factory_production_model.pkl"
model = joblib.load(MODEL_FILE)

# Generate Sample Data
def generate_sample_data():
    """Generates sample production volume data."""
    df = pd.DataFrame([SAMPLE_DATA])
    return df

# Prediction function
def predict_production_volume():
    """Predict production volume using the trained model."""
    try:
        input_data = generate_sample_data()
        predictions = model.predict(input_data)
        input_data["Predicted Production Volume (units)"] = predictions
        return input_data.to_json(orient='records')
    except Exception as e:
        return f"Error in prediction: {e}"

# Execute prediction
result = predict_production_volume()
print(result)
