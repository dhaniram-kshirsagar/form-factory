import streamlit as st
import pandas as pd
import json
import jsonschema
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from utils.revenue_processing import encode_revenue_data
from utils.revenue_rag import create_revenue_rag_layer
from modules.ml.ml_rag import get_model_and_params

# Feature keys and mean values
keys_revenue = [
    "month", "year", "Factory", "Location", "Cycle Time (minutes)", 
    "Product Category", "Waste Generated (kg)", "Production Volume (units)",
    "Water Usage (liters)", "Machine Utilization (%)",
    "Machine Age (years)", "Machine Type", "Supplier", "Operator Experience (years)"
]

values_row_2 = [
    0, 6.521072796934866, 2022.0, 2.0, 2.0, 20.02371829958037, 
    1.0023718299580369, 297.2048896186827, 680.4226195949644, 
    6269.731800766283, 73.59872286079182, 6.0622437511403025, 
    1.0023718299580369, 1.0694033935413245, 4.963446086480569
]

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Chatbot prompt template
prompt = '''
You are a helpful assistant that extracts specific features from natural language queries for factory revenue prediction.
Extract values for these features:
- month: integer (1-12)
- year: integer (2020-2030)
- Factory: string (Factory 1 to Factory 10)
- Location: string (City A to City E)
- Cycle Time (minutes): float
- Product Category: string (A, B, or C)
- Waste Generated (kg): float
- Production Volume (units): float
- Water Usage (liters): float
- Machine Utilization (%): float (0-100)
- Machine Age (years): float
- Machine Type: string (Type A, Type B, or Type C)
- Supplier: string (Supplier A, Supplier B, or Supplier C)
- Operator Experience (years): float

Return JSON with extracted values or empty object if unable to parse.
Always return the full set of features, using default values for any that aren't specified in the query.
'''

def parse_query_to_input(query, default_values):
    final_prompt = prompt.format(query=query)
    try:
        messages = [HumanMessage(content=final_prompt)]
        extracted = llm.invoke(messages).content
        extracted = json.loads(extracted)
        if extracted == {}:
            return {}
        return {**default_values, **extracted}
    except Exception as e:
        print(f"Error parsing query: {e}")
        return {}

def chatbot_prediction(model, query, default_values):
    extracted_data = parse_query_to_input(query, default_values)
    if not extracted_data:
        return None, None, "Unable to extract values from query", extracted_data
    
    input_df = pd.DataFrame([extracted_data])
    input_df = encode_revenue_data(input_df)
    
    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0][1] if hasattr(model, 'predict_proba') else None
    
    rag = create_revenue_rag_layer()
    explanation = rag.run(f"Explain this revenue prediction given inputs: {extracted_data}")
    
    return prediction, proba, explanation, extracted_data

def validate_default_values(data):
    schema = {
        'type': 'object',
        'properties': {
            'month': {'type': 'integer', 'minimum': 1, 'maximum': 12},
            'year': {'type': 'integer', 'minimum': 2020, 'maximum': 2030},
            'Factory': {'type': 'string'},
            'Location': {'type': 'string'},
            'Cycle Time (minutes)': {'type': 'number'},
            'Product Category': {'type': 'string'},
            'Waste Generated (kg)': {'type': 'number'},
            'Production Volume (units)': {'type': 'number'},
            'Water Usage (liters)': {'type': 'number'},
            'Machine Utilization (%)': {'type': 'number', 'minimum': 0, 'maximum': 100},
            'Machine Age (years)': {'type': 'number'},
            'Machine Type': {'type': 'string'},
            'Supplier': {'type': 'string'},
            'Operator Experience (years)': {'type': 'number'}
        },
        'required': ['month', 'year', 'Factory', 'Location', 'Cycle Time (minutes)', 'Product Category', 'Waste Generated (kg)', 'Production Volume (units)', 'Water Usage (liters)', 'Machine Utilization (%)', 'Machine Age (years)', 'Machine Type', 'Supplier', 'Operator Experience (years)'],
        'additionalProperties': False
    }
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True, ""
    except jsonschema.ValidationError as e:
        return False, f"Validation error: {e.message}"

def chatbot_interface(model):
    if 'default_values' not in st.session_state:
        st.session_state.default_values = {
            'month': int(values_row_2[0]),
            'year': int(values_row_2[1]),
            'Factory': str(int(values_row_2[2])),
            'Location': str(int(values_row_2[3])),
            'Cycle Time (minutes)': values_row_2[4],
            'Product Category': str(int(values_row_2[5])),
            'Waste Generated (kg)': values_row_2[6],
            'Production Volume (units)': values_row_2[7],
            'Water Usage (liters)': values_row_2[8],
            'Machine Utilization (%)': values_row_2[9],
            'Machine Age (years)': values_row_2[10],
            'Machine Type': str(int(values_row_2[11])),
            'Supplier': str(int(values_row_2[12])),
            'Operator Experience (years)': values_row_2[13]
        }

    with st.expander("Edit Default Values Configuration", expanded=False):
        default_json = st.text_area(
            "Modify the default values in JSON format:",
            value=json.dumps(st.session_state.default_values, indent=2),
            height=300,
            help="Edit the default values used for chatbot predictions"
        )
        
        if st.button("Update Default Values", use_container_width=True):
            try:
                parsed_values = json.loads(default_json)
                is_valid, error_msg = validate_default_values(parsed_values)
                if is_valid:
                    st.session_state.default_values = parsed_values
                    st.success("Default values updated successfully!")
                else:
                    st.error(error_msg)
            except json.JSONDecodeError:
                st.error("Invalid JSON format. Please check your input.")

    if "messages_astro" not in st.session_state:
        st.session_state.messages_astro = []

    if prompt := st.chat_input("What's the revenue prediction for Factory 2 in March 2025?"):
        if st.session_state.default_values:
            default_values = st.session_state.default_values
        prediction, proba, explanation, extracted_data = chatbot_prediction(model, prompt, default_values)
        
        if prediction is None:
            response = f"**Prediction:** Unable to extract values from query. Revisit your query.\n"
        else:
            response = f"**Predicted Revenue:** ${prediction:,.2f}\n"
        if proba is not None:
            response += f"**Confidence:** {proba:.2%}\n"
        response += f"\n**Explanation:**\n{explanation}\n\n"
        response += "**Extracted Factory Data:**\n```json\n" + json.dumps(extracted_data, indent=2) + "\n"
        
        st.session_state.messages_astro.append({"role": "user", "content": prompt})
        st.session_state.messages_astro.append({"role": "assistant", "content": response})

    for message in st.session_state.messages_astro:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])