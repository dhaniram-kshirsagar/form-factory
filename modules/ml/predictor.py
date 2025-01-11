import joblib
from pathlib import Path

# Configuration (adjust paths as needed)
# PRODUCTION_MODEL_FILE = '/workspaces/form-factory/modules/ml/'+"production_volume_model.pkl"
# REVENUE_MODEL_FILE = '/workspaces/form-factory/modules/ml/'+"revenue_model.pkl"
# FOAM_DENSITY_MODEL_FILE = '/workspaces/form-factory/modules/ml/'+"foam_density_model.pkl"

PRODUCTION_MODEL_FILE = Path(__file__).parent.parent/"ml/production_volume_model.pkl"
REVENUE_MODEL_FILE = Path(__file__).parent.parent/"ml/revenue_model.pkl"
FOAM_DENSITY_MODEL_FILE = Path(__file__).parent.parent/"ml/foam_density_model.pkl"

# Load ML Models (with error handling)
models = {}
model_files = {
    "production_volume_model": PRODUCTION_MODEL_FILE,
    "revenue_model": REVENUE_MODEL_FILE,
    "foam_density_model": FOAM_DENSITY_MODEL_FILE
}
for model_name, file_path in model_files.items():
    try:
        models[model_name] = joblib.load(file_path)
    except FileNotFoundError as e:
        print(f"Error loading model {model_name}: {e}")
        exit()

def getPrediction(model_name, input_data):
    model = models[model_name]
    return model.predict(input_data) 

def get_vol_prediction_for_6month(input_data):
    model = models['production_volume_model']
    return model.predict(input_data) 

def get_rev_prediction_for_6month(input_data):
    model = models['revenue_model']
    return model.predict(input_data) 

def get_foam_prediction_for_6month(input_data):
    model = models['foam_density_model']
    return model.predict(input_data) 