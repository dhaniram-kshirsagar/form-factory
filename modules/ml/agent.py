import datetime
import pandas as pd
import joblib
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.agents import Tool, initialize_agent
import json

# Configuration (adjust paths as needed)
PRODUCTION_MODEL_FILE = "production_volume_model.pkl"
REVENUE_MODEL_FILE = "revenue_model.pkl"
FOAM_DENSITY_MODEL_FILE = "foam_density_model.pkl"
LLM_MODEL = "gpt-3.5-turbo"
ALL_MONTHS = list(range(1, 13))  # All 12 months
ALL_LOCATIONS = [0,1,2,3] # All 4 locations

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

# Generate Sample Data (Multiple Months/Locations)
def generate_sample_data(model_name, years, months, factories, locations):
    """Generates sample data for multiple months and locations."""

    data = []
    for year in years:
      for month in months:
        for factory in factories:
          for location in locations:
            if model_name == "production_volume_model":
                data.append({'Year': year, 'Month': month, 'Factory': factory, 'Location': location})
            elif model_name == "revenue_model":
                data.append({'Year': year, 'Month': month, 'Factory': factory, 'Location': location})
            elif model_name == "foam_density_model":
                data.append({'Year': year, 'Month': month, 'Factory': factory, 'Location': location})

    if not data:
        return None  # Unknown model or empty data

    return pd.DataFrame(data)

# Define Prediction Functions (generalized)
def predict(model_name, years, months, factories, locations):
    """Generalized prediction function for multiple inputs."""
    try:
        model = models[model_name]
        input_data = generate_sample_data(model_name, years, months, factories, locations)
        if input_data is None:
            return "Unknown model name or no data generated."

        predictions = model.predict(input_data)
        input_data['prediction'] = predictions
        return input_data.to_json(orient='records') #Return the result as json string
    except (KeyError, IndexError, ValueError, TypeError) as e:
        return f"Error during prediction for {model_name}: {e}"

# Define Tools (dynamically)
tools = []
model_descriptions_file = "model_descriptions_updated.json"
try:
    with open(model_descriptions_file, 'r') as f:
        model_descriptions = json.load(f)
except FileNotFoundError:
    print(f"Error: {model_descriptions_file} not found. Create this file.")
    exit()

for model_name, model_data in model_descriptions.items():
    tool_name = model_name.replace("_", " ").title().replace("Model", "Predictor")
    description = f"Useful for predicting {model_data['target_variable'].lower()}. Input should be "
    description += ", ".join([f"{feature} ({'integer' if str(feature).lower() in ['year','month'] else 'string'})" for feature in model_data['input_features']]) + "."
    input_params = model_data['input_features']
    tools.append(
        Tool(
            name=tool_name,
            func=lambda year, month, factory, location, model_name=model_name: predict(model_name, year, month, factory, location),
            description=description,
        )
    )

# Initialize Agent
llm = OpenAI(temperature=0, model=LLM_MODEL)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)


def run_agent(model_name, input_params):
    """Runs the agent with the specified model and parameters."""
    try:
        years = input_params.get("years", [])
        months = input_params.get("months", [])
        factories = input_params.get("factories", [])
        locations = input_params.get("locations", [])
        if not years:
          years = [datetime.now().year]
        if not months:
          months = ALL_MONTHS
        if not factories:
          factories = ["Factory 1"] # default factory
        if not locations:
          locations = ALL_LOCATIONS

        prompt_string = f"Predict {model_descriptions[model_name]['target_variable'].lower()} for "
        prompt_string += ", ".join([f"{key} {value}" for key,value in input_params.items()]) + "."
        return agent.run(prompt_string)

    except Exception as e:
        return f"Error running agent: {e}"

# Example Usage
questions = [
    "What will be the production volume in 2024 for all months for factory A in all locations?",
    "Predict the revenue in 2023 for December for factory B in Location Y.",
    "What is the foam density predicted for 2025 February for factory C in location Z?",
    "What will be the production volume in 2024 for factory A in Location A and Location B?", #Example for multiple locations
    "What is the weather like in London?"
]

for question in questions:
    model, params = get_model_and_params(question)
    if model:
        print(f"Question: {question}")
        print(f"Selected Model: {model}")
        print(f"Input Parameters: {params}")
        prediction = run_agent(model, params)
        print(f"Prediction: {prediction}")
        print("-" * 20)
    else:
        print(f"Question: {question}")
        print("No suitable model found.")
        print("-" * 20)