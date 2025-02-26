from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
import json
import os
from pathlib import Path
import pandas as pd
from modules.ml import predictor as predictor
from datetime import datetime

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = ""

FEATURE_COLUMN = ["Year", "Month", "Factory", "Location", "Machine Type", "Machine Utilization (%)", "Machine Downtime (hours)", "Maintenance History", "Machine Age (years)", "Batch Quality (Pass %)", "Cycle Time (minutes)", "Energy Consumption (kWh)", "Energy Efficiency Rating", "CO2 Emissions (kg)", "Emission Limit Compliance", "Waste Generated (kg)", "Water Usage (liters)", "Shift", "Operator Experience (years)", "Team Size", "Operator Training Level", "Absenteeism Rate (%)", "Product Category", "Supplier", "Supplier Delays (days)", "Raw Material Quality", "Market Demand Index", "Cost of Downtime ($)", "Profit Margin (%)", "Breakdowns (count)", "Safety Incidents (count)", "Defect Root Cause", "Production Volume (units)", "Defect Rate (%)", "Foam Density", "Sales Data", "Day"]
PREDICATION_MEAN_DATA = [0.983,75.087384853468,5.1235797895128,0.9932,10.3998,92.721868736494,32.5424621251856,299.331898,1.5288,29.956514000000002,0.4986,10.570336,3020.259442,1.0016,14.8794,6.0178,0.9918,10.005598411952,0.989,1.0148,15.1528,1.0186,0.5008611607164,5435.944922,17.551766,2.0352,2.5354,0.9832,5487.2412,5.008947999999999,1.2468540000000001,27596.527794,15.7162]
PRED_DATA =  dict(zip(FEATURE_COLUMN, PREDICATION_MEAN_DATA))

keys = [
    "Year", "Month", "Factory", "Location", "Machine Type",
    "Machine Utilization (%)", "Machine Downtime (hours)",
    "Maintenance History", "Machine Age (years)",
    "Batch Quality (Pass %)", "Cycle Time (minutes)",
    "Energy Consumption (kWh)", "Energy Efficiency Rating",
    "CO2 Emissions (kg)", "Emission Limit Compliance",
    "Waste Generated (kg)", "Water Usage (liters)",
    "Shift", "Operator Experience (years)",
    "Team Size", "Operator Training Level",
    "Absenteeism Rate (%)", "Product Category",
    "Supplier", "Supplier Delays (days)",
    "Raw Material Quality", "Market Demand Index",
    "Cost of Downtime ($)", "Profit Margin (%)",
    "Breakdowns (count)", "Safety Incidents (count)",
    "Defect Root Cause", "Production Volume (units)",
    "Defect Rate (%)", "Foam Density", 
    "Sales Data", "Day", 
    "Predicted Revenue ($)"
]


values_row_1 = [
    2025, 1, 2, 1, 0.983, 
    75.087384853468, 5.1235797895128, 0.9932, 10.3998, 
    92.721868736494, 32.5424621251856, 299.331898, 
    1.5288, 29.956514000000002, 0.4986, 10.570336,
    3020.259442, 1.0016, 14.8794, 6.0178,
    0.9918, 10.005598411952, 0.989, 1.0148,
    15.1528, 1.0186, 0.5008611607164,
    5435.944922, 17.551766, 2.0352,
    2.5354, 0.9832, 
    5487.2412, 
    5.008947999999999,
    1.2468540000000001,
    27596.527794,
    15.7162,
   -487572.42814425984
]



dict_row_1 = dict(zip(keys, values_row_1))


MODEL_DESCRTIPTIONS_FILE = Path(__file__).parent.parent/"ml/model_descriptions.json"
DATA_DESCRIPTIONS_FILE = Path(__file__).parent.parent/"ml/data_descriptions.json"

LLM_MODEL = "gpt-4"
ALL_MONTHS = list(range(1, 13))  # All 12 months
ALL_LOCATIONS = [0,1,2,3] # All 4 locations

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

def predict(model_name, years, months, factories, locations):
    """Generalized prediction function for multiple inputs."""
    try:
        input_data = generate_sample_data(model_name, years, months, factories, locations)
        if input_data is None:
            return "Unknown model name or no data generated."
        
        predictions = predictor.getPrediction(model_name, input_data)
        input_data['prediction'] = predictions
        
        filtered_data = input_data[['year', 'month', 'Factory', 'Location', 'prediction']]
        
        return filtered_data.to_json(orient='records')  # Return only the filtered data as JSON string
    
    except (KeyError, IndexError, ValueError, TypeError) as e:
        return f"Error during prediction for {model_name}: {e}"

tools = []

try:
    with open(MODEL_DESCRTIPTIONS_FILE, 'r') as f:
        model_descriptions = json.load(f)
except FileNotFoundError:
    print(f"Error: {MODEL_DESCRTIPTIONS_FILE} not found. Create this file.")
    exit()

for model_name, model_data in model_descriptions.items():
    tool_name = model_name
    description = f"Useful for predicting {model_data['target_variable'].lower()}. Input should be "
    description += ", ".join([f"{feature} ({'array of integer' if str(feature).lower() in ['year','month'] else 'array of integer'})" for feature in model_data['input_features']]) + "."
    input_params = model_data['input_features']
    tools.append(
        StructuredTool.from_function(
            name=tool_name,
            func=lambda year, month, factory, location, model_name=model_name: predict(model_name, year, month, factory, location),
            description=description
        )
    )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         """
         You are an advanced ML model assistant. Your job is to predict values based on the given data
         and always provide the output in the requested format.

        1. Example of incorrect intermidiate input for given question-
        Question:
        Predict production volume (units) for years [2025], months [1, 2, 3, 4, 5], factories [2], locations [0]
        
        Incorrect intermidiate output:
        `production_volume_model` with `{{'year': [2025, 2025, 2025, 2025, 2025], 'month': [1, 2, 3, 4, 5], 'factory': [2, 2, 2, 2, 2], 'location': [0, 0, 0, 0, 0]}}`

        Correct intermidiate output:
        `production_volume_model` with `{{'year': [2025], 'month': [1, 2, 3, 4, 5], 'factory': [2], 'location': [0]}}`

         Make sure the output strictly adheres to the specified format. If the user provides custom output requirements,
         adjust your response accordingly.

         Output Format:  {{"Predicted_data":ml_model_output_dataframe, "llm_output_text_summmary":Text Summary}}

         NOTE - Strictly avoid including input in the output.
         
         """),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent_executor = None

def init(llm):
    global agent_executor
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def run_agent(model_name, input_params):
    """Runs the agent with the specified model and parameters."""
   
    years = input_params['years']
    months = input_params.get("months", [])
    factories = input_params.get("factories", [])
    locations = input_params.get("locations", [])

    if not years:
        years = [datetime.now().year]
    if not months:
        months = ALL_MONTHS
    if not factories:
        factories = [0] # default factory
    if not locations:
        locations = ALL_LOCATIONS
    
    prompt_string = f"Predict {model_descriptions[model_name]['target_variable'].lower()} for "
    prompt_string += ", ".join([f"{key} {value}" for key,value in input_params.items()]) + "."

    print(prompt_string)
    return agent_executor.invoke({"input":prompt_string})