import joblib
import pandas as pd
from pathlib import Path
from modules.ml.feature_registry import FeatureRegistry

feature_registry = FeatureRegistry()

keys_revenue = ["month","year","Factory","Cycle Time (minutes)","Product Category","Waste Generated (kg)","Production Volume (units)","Water Usage (liters)","Machine Utilization (%)","Machine Age (years)","Machine Type","Supplier","Operator Experience (years)"]
keys_prod_volume = ["month", "year","Factory", "Machine Utilization (%)", "Operator Experience (years)", "Market Demand Index", "Breakdowns (count)", "Absenteeism Rate (%)", "Raw Material Quality",  "Revenue ($)", "Batch Quality (Pass %)", "Cost of Downtime ($)"]
keys_prof_margin = ["month", "year", "Factory", "CO2 Emissions (kg)", "Energy Consumption (kWh)", "Product Category", "Supplier", "Machine Type", "Machine Utilization (%)", "Water Usage (liters)"]
revs_mean_values_row_2 = [0, 6.521072796934866, 2022.0, 2.0, 20.02371829958037, 1.0023718299580369, 297.2048896186827, 680.4226195949644, 6269.731800766283, 73.59872286079182, 6.0622437511403025, 1.0023718299580369, 1.0694033935413245, 4.963446086480569]
prodvol_mean_values_row_2 = [0, 6.521072796934866, 2022.0, 2.0, 73.59872286079182, 4.963446086480569, 96.77613574165298, 3.7264349571246123, 3.0199069512862615, 0.4005108556832695, 429484.10147162934, 90.36329246487867, 9786.44189819376, 680.4226195949644]
prof_margin_mean_values_row_2 = [0, 6.521072796934866, 2022.0, 2.0, 696.4505017332604, 652.7277869002007, 1.0023718299580369, 1.0694033935413245, 1.0023718299580369, 73.59872286079182, 6269.731800766283, 21.426483853311442]

rev_mean_dict = dict(zip(keys_revenue, revs_mean_values_row_2))
prodvol_mean_dict = dict(zip(keys_prod_volume, prodvol_mean_values_row_2))
prof_margin_mean_dict = dict(zip(keys_prof_margin, prof_margin_mean_values_row_2))

# Configuration
REVENUE_MODEL_FILE = Path(__file__).parent.parent/"ml/revenue_prediction_model.pkl"
PRODUCTION_VOLUME_MODEL_FILE = Path(__file__).parent.parent/"ml/prod_volume_prediction_model.pkl"
PROFIT_MARGIN_PREDICTION_MODEL_FILE = Path(__file__).parent.parent/"ml/prof_margin_prediction_model.pkl"

# Load ML Models (with error handling)
class Predictor:
    def __init__(self):
        self.models = self._load_models()

    def _load_models(self):
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
        return models

    def predict(self, model_name: str, input_data: pd.DataFrame) -> pd.DataFrame:
        # Validate features
        feature_status = feature_registry.validate_features(model_name, input_data)
        missing_features = [f for f, present in feature_status.items() if not present]
        
        if missing_features:
            raise ValueError(f"Missing required features: {', '.join(missing_features)}")
        
        return self.models[model_name].predict(input_data)

astro_predictor = Predictor()

def getPrediction(model_name, input_data):
    print("Input received for prediction: \n"+input_data.to_csv(index=False))
    return astro_predictor.predict(model_name, input_data)

def get_rev_prediction_for_6month(input_data):
    print("Revenue prediction with categorical filters:")
    print(input_data.to_csv(index=False))
    # Extract categorical features for debugging
    categorical_features = input_data[['Product Category', 'Machine Type', 'Supplier']].iloc[0].to_dict()
    print(f"Categorical features used: {categorical_features}")
    return astro_predictor.predict('revenue_model', input_data)

def get_vol_prediction_for_6month(input_data):
    print("Production volume prediction with categorical filters:")
    print(input_data.to_csv(index=False))
    # Extract categorical features for debugging
    categorical_features = input_data[['Raw Material Quality']].iloc[0].to_dict()
    print(f"Categorical features used: {categorical_features}")
    return astro_predictor.predict('production_volume_model', input_data)

def get_foam_prediction_for_6month(input_data):
    print("Profit margin prediction with categorical filters:")
    print(input_data.to_csv(index=False))
    # Extract categorical features for debugging
    categorical_features = input_data[['Product Category', 'Supplier', 'Machine Type']].iloc[0].to_dict()
    print(f"Categorical features used: {categorical_features}")
    return astro_predictor.predict('profit_margin_model', input_data)

def get_mean_value(model_name: str, feature: str) -> float:
        """Get the mean value of a feature for a given model.
        
        Args:
            model_name (str): Name of the model
            feature (str): Name of the feature
        
        Returns:
            float: Mean value of the feature
        """
        if model_name == 'production_volume_model':
            return prodvol_mean_dict.get(feature, 0)
        elif model_name == 'revenue_model':
            return rev_mean_dict.get(feature, 0)
        elif model_name == 'profit_margin_model':
            return prof_margin_mean_dict.get(feature, 0)
        return 0
        
# Get categorical feature values for each model
def get_categorical_feature_values(model_name: str) -> dict:
    """Get the categorical feature values for a given model.
    
    Args:
        model_name (str): Name of the model
    
    Returns:
        dict: Dictionary of categorical features and their possible values
    """
    if model_name == 'production_volume_model':
        return {
            'Raw Material Quality': [0, 1, 2]  # Low, Medium, High
        }
    elif model_name == 'revenue_model':
        return {
            'Product Category': [0, 1, 2, 3],  # Different product categories
            'Machine Type': [0, 1, 2],         # Different machine types
            'Supplier': [0, 1, 2, 3]           # Different suppliers
        }
    elif model_name == 'profit_margin_model':
        return {
            'Product Category': [0, 1, 2, 3],  # Different product categories
            'Supplier': [0, 1, 2, 3],          # Different suppliers
            'Machine Type': [0, 1, 2]          # Different machine types
        }
    return {}