from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
import json
import os

from pathlib import Path
import pandas as pd

from modules.ml import predictor

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

# Define the values for the first row
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

#print(PRED_DATA)

#MODEL_DESCRTIPTIONS_FILE = '/workspaces/form-factory/modules/ml/'+"model_descriptions.json"
MODEL_DESCRTIPTIONS_FILE = Path(__file__).parent.parent/"ml/model_descriptions.json"

LLM_MODEL = "gpt-4"
ALL_MONTHS = list(range(1, 13))  # All 12 months
ALL_LOCATIONS = [0,1,2,3] # All 4 locations



# Generate Sample Data (Multiple Months/Locations)
def generate_sample_data(model_name, years, months, factories, locations):
    """Generates sample data for multiple months and locations."""

    future_data = pd.DataFrame()
    for year in years:
        for month in months:
            for factory in factories:
                for location in locations:
                    temp_data = pd.DataFrame({
                        'Year': [year],
                        'Month': month,
                        'Factory': [factory],
                        'Location': [location]
                    })
                    for col in FEATURE_COLUMN:
                        if col not in temp_data.columns:
                            temp_data[col] = dict_row_1[col]

                    future_data = pd.concat([future_data, temp_data], ignore_index=True)

    return future_data

# Define Prediction Functions (generalized)
def predict(model_name, years, months, factories, locations):
    """Generalized prediction function for multiple inputs."""
    try:
        
        input_data = generate_sample_data(model_name, years, months, factories, locations)
        if input_data is None:
            return "Unknown model name or no data generated."
        
        predictions = predictor.getPrediction(model_name, input_data)
        input_data['prediction'] = predictions
        return input_data.to_json(orient='records') #Return the result as json string
    except (KeyError, IndexError, ValueError, TypeError) as e:
        return f"Error during prediction for {model_name}: {e}"

# Define Tools (dynamically)
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
    #print(description)
    tools.append(
        StructuredTool.from_function(
            name=tool_name,
            func=lambda year, month, factory, location, model_name=model_name: predict(model_name, year, month, factory, location),
            description=description
        )
    )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a ml model prediction assistant. Use input as it is. Don't break numbers in multiple prediction call. "),
        ("placeholder", "{chat_history}"),
        # Then the new input
        ("human", "{input}"),
        # Finally the scratchpad
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
    
    #print('Starting agent run3')

    prompt_string = f"Predict {model_descriptions[model_name]['target_variable'].lower()} for "
    prompt_string += ", ".join([f"{key} {value}" for key,value in input_params.items()]) + "."

    print(prompt_string)
    return agent_executor.invoke({"input":prompt_string})


#data = run_agent('foam_density_model', '{"years": [2025], "months": [1, 4], "factories": [0], "locations": [0]}')
# for d in data['output']:
#     print(d)
#print(data['output'])
# Example Usage
# questions = [
#     "What will be the production volume in 2024 for all months for factory A in all locations?",
#     "Predict the revenue in 2023 for December for factory B in Location Y.",
#     "What is the foam density predicted for 2025 February for factory C in location Z?",
#     "What will be the production volume in 2024 for factory A in Location A and Location B?", #Example for multiple locations
#     "What is the weather like in London?"
# ]

# for question in questions:
#     model, params = get_model_and_params(question)
#     if model:
#         print(f"Question: {question}")
#         print(f"Selected Model: {model}")
#         print(f"Input Parameters: {params}")
#         prediction = run_agent(model, params)
#         print(f"Prediction: {prediction}")
#         print("-" * 20)
#     else:
#         print(f"Question: {question}")
#         print("No suitable model found.")
#         print("-" * 20)

# df = generate_sample_data("test", [2025, 2026], [2, 4, 5, 7], [1], [3, 0, 1])
# df.to_csv("tesdataaaa.csv", index=False)