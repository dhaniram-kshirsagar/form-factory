import streamlit as st
import pandas as pd
import json
import jsonschema
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from utils.data_processing import encode_data_7
from utils.rag import create_rag_layer

prompt = '''
You are a helpful assistant that extracts specific features from natural language queries for churn prediction. 
Extract values only for these features:
- 'tenure': integer (minimum: 0)
- 'OnlineSecurity': string (enum: ['Yes', 'No', 'No internet service'])
- 'OnlineBackup': string (enum: ['Yes', 'No', 'No internet service'])
- 'TechSupport': string (enum: ['Yes', 'No', 'No internet service'])
- 'Contract': string (enum: ['Month-to-month', 'One year', 'Two year'])
- 'MonthlyCharges': number (minimum: 0)
- 'TotalCharges': number (minimum: 0)

Rules:
1. Return only valid JSON containing extracted values
2. If unable to map any fields, return {{}}
3. Do not include any explanations, notes, or additional text
4. Maintain exact JSON format: {{"key": value}}

Examples:
{{"tenure": 3, "OnlineSecurity": "No", "OnlineBackup": "No", "TechSupport": "No", "Contract": "Month-to-month", "MonthlyCharges": 70.35, "TotalCharges": 211.05}}
or
{{"tenure": 1}}

Question: {query}
Output:
'''

from langchain.prompts.prompt import PromptTemplate


prompt = PromptTemplate(
        input_variables=["query"],
        template=prompt,
    )
llm = ChatOpenAI(model="gpt-4", temperature=0)

from langchain.schema import HumanMessage


def parse_query_to_input(query, default_values):
    print('Starting parse_query_to_input')
    print('Query:', query)
    """Parse natural language query into structured input using LLM"""


    final_prompt = prompt.format(query=query)


    try:
        messages = [HumanMessage(content=final_prompt)] # Create a list of messages
        extracted = llm.invoke(messages).content
        print('Extracted data:', extracted)
        extracted = json.loads(extracted)
        print('Extracted data:', type(extracted), extracted)
        if extracted == {}:
            print('Unable to extract values from query')
            return {}
        # Merge extracted values with defaults
        return {**default_values, **extracted}
    except Exception as e:
        print('Unable to parse response', e)
        return {}

def chatbot_prediction(model, query, default_values):
    print('Starting chatbot_prediction')
    print('Query:', query)
    """Handle chatbot queries for churn prediction with LLM parsing"""
    # Parse query to get specific values
    extracted_data = parse_query_to_input(query, default_values)
    print('Final data for encoding:', extracted_data)
    if not extracted_data:
        return None, None, "Unable to extract values from query", extracted_data
    # Create dataframe and preprocess
    input_df = pd.DataFrame([extracted_data])
    input_df = encode_data_7(input_df)
    print('Encoded DataFrame:', input_df.head())
    clean_columns = ['tenure', 'OnlineSecurity', 'OnlineBackup', 'TechSupport', 'Contract', 'MonthlyCharges', 'TotalCharges']
    input_df =  input_df[clean_columns]
    # Make prediction
    prediction = model.predict(input_df)[0]
    print('Prediction:', prediction)
    proba = model.predict_proba(input_df)[0][1] if hasattr(model, 'predict_proba') else None
    print('Probability:', proba)

    # Generate explanation using RAG
    rag = create_rag_layer()
    explanation = rag.run(f"Explain why this customer might {'churn' if prediction == 1 else 'not churn'} given inputs are {extracted_data}")
    print('Explanation:', explanation)

    return prediction, proba, explanation, extracted_data
    print('Completed chatbot_prediction')

def validate_default_values(data):
    print('Starting validate_default_values')
    print('Input data:', data)
    """Validate the structure and content of default values"""
    schema = {
        'type': 'object',
        'properties': {
            'tenure': {'type': 'integer', 'minimum': 0},
            'OnlineSecurity': {'type': 'string', 'enum': ['Yes', 'No', 'No internet service']},
            'OnlineBackup': {'type': 'string', 'enum': ['Yes', 'No', 'No internet service']},
            'TechSupport': {'type': 'string', 'enum': ['Yes', 'No', 'No internet service']},
            'Contract': {'type': 'string', 'enum': ['Month-to-month', 'One year', 'Two year']},
            'MonthlyCharges': {'type': 'number', 'minimum': 0},
            'TotalCharges': {'type': 'number', 'minimum': 0}
        },
        'required': ['tenure', 'OnlineSecurity', 'OnlineBackup', 'TechSupport', 'Contract', 'MonthlyCharges', 'TotalCharges'],
        'additionalProperties': False
    }
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True, ""
    except jsonschema.ValidationError as e:
        return False, f"Validation error: {e.message}"
    print('Completed validate_default_values')

def chatbot_interface(model):
    print('Starting chatbot_interface')
    """Handle the chatbot UI and interactions"""
    # Initialize default values
    if 'default_values' not in st.session_state:
        st.session_state.default_values = {
            'tenure': 3,
            'OnlineSecurity': 'No',
            'OnlineBackup': 'No',
            'TechSupport': 'No',
            'Contract': 'Two year',
            'MonthlyCharges': 164.76,
            'TotalCharges': 2283.30
        }

    # Main area for default values
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

    # Initialize chat history
    if "messages_astro" not in st.session_state:
        st.session_state.messages_astro = []

    # Display chat messages from history on app rerun
    # for message in st.session_state.messages_astro:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Churn possibility if customer stays more than 10 months?"):
        # Add user message to chat history
        #st.session_state.messages_astro.append({"role": "user", "content": prompt})
       
        # Display user message in chat message container
        # with st.chat_message("user"):
        #     st.markdown(prompt)

        # Get prediction and explanation
        if st.session_state.default_values:
            default_values = st.session_state.default_values
        prediction, proba, explanation, extracted_data = chatbot_prediction(model, prompt, default_values)
        
        # Format response
        if prediction is None:
            response = f"**Prediction:** Unable to extract values from query. Revisit your query.\n"
        else:
            response = f"**Prediction:** {'Churn' if prediction == 1 else 'No Churn'}\n"
        if proba is not None:
            response += f"**Probability of Churn:** {proba:.2%}\n"
        response += f"\n**Explanation:**\n{explanation}\n\n"
        response += "**Extracted Customer Data:**\n```json\n" + json.dumps(extracted_data, indent=2) + "\n"
        
        # Display assistant response in chat message container
        # with st.chat_message("assistant"):
        #     st.markdown(response)
        
        # Add assistant response to chat history
        #st.session_state.messages_astro.append({"role": "assistant", "content": response})

        st.session_state.messages_astro.append(('You', prompt))
        st.session_state.messages_astro.append(('Bot', response))
    
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container"><h5>Chat History</h5>', unsafe_allow_html=True)
        for i in range(len(st.session_state.messages_astro)-1, -1, -2):
            if i-1 >= 0:
                bot_role, bot_msg = st.session_state.messages_astro[i-1]
                with st.chat_message("assistant"):
                    st.markdown(f'<div class="chat-message {bot_role.lower()}"><strong>{bot_role}</strong>: {bot_msg}</div>', unsafe_allow_html=True)
            if i >= 0:
                user_role, user_msg = st.session_state.messages_astro[i]
                with st.chat_message("user"):
                    st.markdown(f'<div class="chat-message {user_role.lower()}"><strong>{user_role}</strong>: {user_msg} </div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


    print('Completed chatbot_interface')
