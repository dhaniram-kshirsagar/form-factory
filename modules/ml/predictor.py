import joblib
from pathlib import Path


keys_revenue = ["month","year","Factory","Cycle Time (minutes)","Product Category","Waste Generated (kg)","Production Volume (units)",
    "Water Usage (liters)","Machine Utilization (%)",
    "Machine Age (years)","Machine Type","Supplier","Operator Experience (years)"
]

keys_prod_volume = ["month", "year","Factory", "Machine Utilization (%)", "Operator Experience (years)", "Market Demand Index", "Breakdowns (count)", "Absenteeism Rate (%)", "Raw Material Quality",  "Revenue ($)", "Batch Quality (Pass %)", "Cost of Downtime ($)"]
keys_prof_margin = ["month", "year", "Factory", "CO2 Emissions (kg)", "Energy Consumption (kWh)", "Product Category", "Supplier", "Machine Type", "Machine Utilization (%)", "Water Usage (liters)"]
revs_mean_values_row_2 = [0
6.521072796934866
2022.0
2.0
20.02371829958037
1.0023718299580369
297.2048896186827
680.4226195949644
6269.731800766283
73.59872286079182
6.0622437511403025
1.0023718299580369
1.0694033935413245
4.963446086480569
429484.10147162934
]

prodvol_mean_values_row_2 = [0,
    6.521072796934866,
    2022.0,
    2.0,
    73.59872286079182,
    4.963446086480569,
    96.77613574165298,
    3.7264349571246123,
    3.0199069512862615,
    0.4005108556832695,
    429484.10147162934,
    90.36329246487867,
    9786.44189819376,
    680.4226195949644
]

prof_margin_mean_values_row_2 = [0,
    6.521072796934866,
    2022.0,
    2.0,
    696.4505017332604,
    652.7277869002007,
    1.0023718299580369,
    1.0694033935413245,
    1.0023718299580369,
    73.59872286079182,
    6269.731800766283,
    21.426483853311442
]


rev_mean_dict = dict(zip(keys_revenue, revs_mean_values_row_2))
prodvol_mean_dict = dict(zip(keys_prod_volume, prodvol_mean_values_row_2))
prof_margin_mean_dict = dict(zip(keys_prof_margin, prof_margin_mean_values_row_2))

# Configuration
REVENUE_MODEL_FILE = Path(__file__).parent.parent/"ml/revenue_prediction_model.pkl"

PRODUCTION_VOLUME_MODEL_FILE = Path(__file__).parent.parent/"ml/prod_volume_prediction_model.pkl"
PROFIT_MARGIN_PREDICTION_MODEL_FILE = Path(__file__).parent.parent/"ml/prof_margin_prediction_model.pkl"

# Load ML Models (with error handling)
models = {}
model_files = {
    "revenue_model": REVENUE_MODEL_FILE,
    "production_volume_model": PRODUCTION_VOLUME_MODEL_FILE,
    "profit_margin_model": PROFIT_MARGIN_PREDICTION_MODEL_FILE
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
    model = models['profit_margin_model']
    return model.predict(input_data)
