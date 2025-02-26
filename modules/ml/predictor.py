import joblib
from pathlib import Path


keys_revenue = ["month","year","Factory","Location","Cycle Time (minutes)","Product Category","Waste Generated (kg)","Production Volume (units)",
    "Water Usage (liters)","Machine Utilization (%)",
    "Machine Age (years)","Machine Type","Supplier","Operator Experience (years)"
]

values_row_2 = [0,
    6.521072796934866,
    2022.0,
    2.0,
    2.0,
    20.02371829958037,
    1.0023718299580369,
    297.2048896186827,
    680.4226195949644,
    6269.731800766283,
    73.59872286079182,
    6.0622437511403025,
    1.0023718299580369,
    1.0694033935413245,
    4.963446086480569
]

rev_mean_dict = dict(zip(keys_revenue, values_row_2))
# Configuration
REVENUE_MODEL_FILE = Path(__file__).parent.parent/"ml/revenue_prediction_model.pkl"

PRODUCTION_MODEL_FILE = Path(__file__).parent.parent/"ml/production_volume_model.pkl"
FOAM_DENSITY_MODEL_FILE = Path(__file__).parent.parent/"ml/foam_density_model.pkl"

# Load ML Models (with error handling)
models = {}
model_files = {
    "revenue_model": REVENUE_MODEL_FILE,
    "production_volume_model": PRODUCTION_MODEL_FILE,
    "foam_density_model": FOAM_DENSITY_MODEL_FILE
}
for model_name, file_path in model_files.items():
    try:
        models[model_name] = joblib.load(file_path)
    except FileNotFoundError as e:
        print(f"Error loading model {model_name}: {e}")
        exit()

def getPrediction(model_name, input_data):
    print(input_data.to_csv(index=False))
    model = models[model_name]
    return model.predict(input_data)

def get_rev_prediction_for_6month(input_data):
    model = models['revenue_model']
    return model.predict(input_data)

def get_vol_prediction_for_6month(input_data):
    model = models['production_volume_model']
    return model.predict(input_data)

def get_foam_prediction_for_6month(input_data):
    model = models['foam_density_model']
    return model.predict(input_data)
