import pandas as pd
import joblib
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
import json
import os

# Configuration (adjust paths as needed)
PRODUCTION_DATA_FILE = "production_data.csv"
PROFIT_DATA_FILE = "profit_data.csv"
MACHINE_DATA_FILE = "machine_data.csv"
PRODUCTION_MODEL_FILE = "production_model.pkl"
PROFIT_MODEL_FILE = "profit_model.pkl"
BREAKDOWN_MODEL_FILE = "breakdown_model.pkl"
LLM_MODEL = "gpt-3.5-turbo"

# Load DataFrames
try:
    df_production = pd.read_csv(PRODUCTION_DATA_FILE)
    df_profit = pd.read_csv(PROFIT_DATA_FILE)
    df_machine = pd.read_csv(MACHINE_DATA_FILE)
except FileNotFoundError as e:
    print(f"Error loading data: {e}")
    exit()

# Load ML Models
try:
    production_model = joblib.load(PRODUCTION_MODEL_FILE)
    profit_model = joblib.load(PROFIT_MODEL_FILE)
    breakdown_model = joblib.load(BREAKDOWN_MODEL_FILE)
except FileNotFoundError as e:
    print(f"Error loading model: {e}")
    exit()

# Define Tools
def predict_production(date, factory_id, shift):
    """Predicts production volume."""
    try:
        input_data = df_production[(df_production['date'] == date) & (df_production['factory_id'] == int(factory_id)) & (df_production['shift'] == shift)]
        if input_data.empty:
            return "No data found for the given date, factory ID, and shift."
        prediction = production_model.predict(input_data)
        return str(prediction[0]) # Convert numpy array to string
    except Exception as e:
        return f"Error during production prediction: {e}"

def predict_profit(market_demand_index, production_volume):
    """Predicts profit margin."""
    try:
        input_data = pd.DataFrame({'market_demand_index': [float(market_demand_index)], 'production_volume': [int(production_volume)]})
        prediction = profit_model.predict(input_data)
        return str(prediction[0])
    except Exception as e:
        return f"Error during profit prediction: {e}"

def predict_breakdown(date, machine_id):
    """Predicts breakdowns."""
    try:
        input_data = df_machine[(df_machine['date'] == date) & (df_machine['machine_id'] == machine_id)]
        if input_data.empty:
            return "No data found for the given date and machine ID."
        prediction = breakdown_model.predict(input_data)
        return str(prediction[0])
    except Exception as e:
        return f"Error during breakdown prediction: {e}"


tools = [
    Tool(
        name="ProductionPredictor",
        func=predict_production,
        description="Useful for predicting production volume. Input should be date (YYYY-MM-DD), factory_id (integer), and shift (string).",
    ),
    Tool(
        name="ProfitPredictor",
        func=predict_profit,
        description="Useful for predicting profit margin. Input should be market_demand_index (float) and production_volume (integer).",
    ),
    Tool(
        name="BreakdownPredictor",
        func=predict_breakdown,
        description="Useful for predicting breakdowns. Input should be date (YYYY-MM-DD) and machine_id (string).",
    )
]

# Initialize Agent
llm = OpenAI(temperature=0, model=LLM_MODEL)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

def run_agent(model_name, input_params):
    """Runs the agent with the specified model and parameters."""
    try:
        if model_name == "production_model":
            return agent.run(f"Predict production volume for date {input_params[0]}, factory id {input_params[1]} and shift {input_params[2]}.")
        elif model_name == "profit_model":
            return agent.run(f"Predict profit margin for market demand index {input_params[0]} and production volume {input_params[1]}.")
        elif model_name == "breakdown_model":
             return agent.run(f"Predict breakdowns for date {input_params[0]} and machine id {input_params[1]}.")
        else:
            return "Unknown model name."
    except Exception as e:
        return f"Error running agent: {e}"