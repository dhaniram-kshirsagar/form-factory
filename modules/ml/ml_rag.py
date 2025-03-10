from concurrent.futures import wait
import json
import re
from datetime import datetime
import streamlit as st

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

import os
from pathlib import Path
import pandas as pd
from typing import Dict
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()
# st.session_state.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# print("OpenAI API key loaded successfully.")

VECTOR_DB_PATH = Path(__file__).parent.parent/"ml/factory_vector_db"
EMBEDDINGS_MODEL = "all-mpnet-base-v2"


# if "OPENAI_API_KEY" not in os.environ:
#     os.environ["OPENAI_API_KEY"] = ""

LLM_MODEL = "gpt-4"
 # LLM Call
llm = ChatOpenAI(temperature=0, model=LLM_MODEL)

# from feature_registry import FeatureRegistry
# import agent

from modules.ml.feature_registry import FeatureRegistry
from modules.ml import agent

feature_registry = FeatureRegistry()

agent.init(llm)

# Updated prompt template with feature awareness and examples
PROMPT_TEMPLATE = '''
You are an expert system designed to select the best machine learning model and extract input parameters to answer user questions about foam factory data.
Your tasks are:
1. Understand the user's query and identify the relevant prediction model
2. Extract parameters based on the model's required features
3. Return the model name and parameters in JSON format

Question: {question}

Relevant Information:
{context}

Instructions:
1. Analyze the question and the provided information.
2. Select the most appropriate ML model to answer the question. If no suitable model is found, respond with "No suitable model found."
3. Extract the necessary input parameters/variables from the question and provided information. 
4. Return the selected model name and the input parameters in JSON format. If no suitable model is found, return "No suitable model found."
5. In output, year should be number like 2025, month should be 1 to 12, factories should be 0 to 4
6. if default values in case following are not mentioned: factories: [0], years:[2025], months:[1]
7. Strictly return output in format listed under 'Output Format:' section
6. Use this mapping:
    Factories:
        Factory 1 -> 0
        Factory 2 -> 1
        ...
        Factory 5 -> 4

Examples:
Examples for Production Volume Model
1. Question: Predict production volume for March with 75% machine utilization and 5 years operator experience
Output: {{"model_name": "production_volume_model", "input_parameters": {{
    "Machine Utilization (%)": 75, 
    "Operator Experience (years)": 5,
    "Months": [3],
    "Years": [2025],
    "Factories": [1]
}}}}

2. Question: Estimate production volume for March and April across factories 1 and 2 with 90% machine utilization
Output: {{"model_name": "production_volume_model", "input_parameters": {{
    "Machine Utilization (%)": 90,
    "Months": [3, 4],
    "Years": [2025],
    "Factories": [1, 2]
}}}}

3. Question: Predict production volume for March with 75% machine utilization and 5 years operator experience
Output: {{"model_name": "production_volume_model", "input_parameters": {{
    "Machine Utilization (%)": 75, 
    "Operator Experience (years)": 5,
    "months": [3],
    "years": [2025],
    "factories": [0]
}}}}

Examples for Revenue Model
3. Question: Forecast revenue for Q1 (Jan-Mar) across all factories with 5000 units production volume
Output: {{"model_name": "revenue_model", "input_parameters": {{
    "Production Volume (units)": 5000,
    "Months": [1, 2, 3],
    "Years": [2025],
    "Factories": [0, 1, 2, 3]
}}}}

4. Question: Predict revenue for June and July in factories 2 and 3 with 90% machine utilization
Output: {{"model_name": "revenue_model", "input_parameters": {{
    "Machine Utilization (%)": 90,
    "Months": [6, 7],
    "Years": [2025],
    "Factories": [2, 3]
}}}}

Examples for Profit Margin Model
5. Question: Estimate profit margin for Q2 (Apr-Jun) in factory 1 with 500 kg CO2 emissions
Output: {{"model_name": "profit_margin_model", "input_parameters": {{
    "CO2 Emissions (kg)": 500,
    "Months": [4, 5, 6],
    "Years": [2025],
    "Factories": [1]
}}}}

6. Question: Predict profit margin for September and October across factories 1, 2 and 3
Output: {{"model_name": "profit_margin_model", "input_parameters": {{
    "Months": [9, 10],
    "Years": [2025],
    "Factories": [1, 2, 3]
}}}}

**General Instructions:**

*   Select the most appropriate ML model to answer the question. If no suitable model is found, respond with "No suitable model found."
*   Extract the necessary input parameters/variables from the question and provided information. 
*   Return the selected model name and the input parameters in JSON format. If no suitable model is found, return "No suitable model found."
*   In output, year should be number like 2025, month should be 1 to 12, factories should be 0 to 4 and locations should be 0 to 4
*   In case year(s), month(s), factorie(s) or location(s) are not mentioned in question then use following: factories: [0], years:[2025], months:[1]
*   Strictly return output in format listed under 'Output Format:' section
*   Handle empty results gracefully by stating that no data is available.

Output Format:

{{"model_name": "model_name", "input_parameters": {{"years":[year],"months":[month],"factories":[factory]}}}}

or

No suitable model found.
'''

def get_model_and_params(question):
    
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)
    try:
        vector_db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        print(f"Error loading vector DB: {e}")
        return None, None

    # Retrieval
    docs = vector_db.similarity_search(question, k=5)
    context = "\n".join([doc.page_content for doc in docs])

    # Prompt Engineering
    prompt = PROMPT_TEMPLATE # Use the externally defined prompt
    if isinstance(prompt, str):
      prompt = PromptTemplate(
          input_variables=["question", "context"],
          template=prompt,
      )
    final_prompt = prompt.format(question=question, context=context)

    try:
        messages = [HumanMessage(content=final_prompt)] # Create a list of messages
        llm_output = llm.invoke(messages).content

        print('llm output:\n '+str(llm_output))

        import regex
        pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
        llm_output = pattern.findall(str(llm_output))

        print('llm json output:\n '+str(llm_output))

        response = json.loads(llm_output[0])
        
        if "model_name" in response and "input_parameters" in response:
            final_params = response["input_parameters"]
            return response["model_name"], final_params
        else:
            print("LLM output is not in the expected JSON format:")
            print(llm_output)
            return None, None

    except json.JSONDecodeError:
        if "No suitable model found." in llm_output:
            return None, None
        else:
            print("Error decoding JSON from LLM output:")
            print(llm_output)
            return None, None
        
def get_ml_answer(query):
    #ToBeFix
    ##### Known issue for rag are
    #########1. output from llm is sometime produces text+json. temp fix applied to just get json. solution -> update prompt to just produce json always
    ##### Known issue for agent are
    #########1. output sent to llm by agent for final result phrasing is huge and goes beyond max tokens supported in cases where you want prediction for multiple years. 
                # e.g. query = "What will be foam density of factory 1 in city A for next 2 years?"
                #soluntion-> just sent input and predicated values
    
    #query = "What will be production volume over next 2 months?"
    #query = "What will be foam density of factory 1 in city A?"
    #query = "What will be revenue over next 2 months for factory 3 in city c?"
    print(query)
    model_name, model_params = get_model_and_params(query)
    print(str(model_name)+' '+str(model_params))
    if model_name is not None:
        data = agent.run_agent(model_name, **model_params)
    else:
        data = 'Unable to map model for given query!!'
    
    print(data)
    return data['output']

def get_ml_answer_with_feedback(model_name: str, input_data: pd.DataFrame) -> Dict:
    # Check feature completeness
    feature_status = feature_registry.validate_features(model_name, input_data)
    missing_features = [f for f, present in feature_status.items() if not present]
    
    # Display feature status
    if missing_features:
        st.warning(f"Missing features: {', '.join(missing_features)}")
        st.info("Using mean values for missing features")
    
    # Get feature importance visualization
    feature_importance = feature_registry.get_feature_importance(model_name)
    if feature_importance:
        st.subheader("Feature Importance")
        st.bar_chart(feature_importance)
    
    # Make prediction
    try:
        prediction = agent.run_agent(model_name, input_data)
        return {
            'status': 'success',
            'prediction': prediction,
            'feature_status': feature_status,
            'feature_importance': feature_importance
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

# if __name__ == "__main__":
#     # Test queries
#     queries = [
#         #"Predict production volume for March with 75% machine utilization and 5 years operator experience",
#          "Estimate profit margin with 500 kg CO2 emissions, 3000 kWh energy consumption, and 90% machine utilization",
#          "Forecast revenue with 5000 units production volume, 3000 kWh energy consumption, and 80% machine utilization"
#     ]
    
#     # Test each query
#     for query in queries:
#         print(f"Query: {query}")
#         try:
#             result = get_ml_answer(query)
#             print(f"Result: {result}")
#             print()
#         except Exception as e:
#             print(f"Error processing query: {e}")
#             print()