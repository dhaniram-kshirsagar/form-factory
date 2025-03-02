from concurrent.futures import wait
import json
import re
from datetime import datetime

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

import os
from pathlib import Path

# --- Configuration ---
#VECTOR_DB_PATH = '/workspaces/form-factory/modules/ml/'+"factory_vector_db"
VECTOR_DB_PATH = Path(__file__).parent.parent/"ml/factory_vector_db"
EMBEDDINGS_MODEL = "all-mpnet-base-v2"


if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = ""

LLM_MODEL = "gpt-4"
 # LLM Call
llm = ChatOpenAI(temperature=0, model=LLM_MODEL)

from modules.ml import agent

agent.init(llm)

MODEL_SELECTION_PROMPT = """
You are an expert system designed to select the best machine learning model and extract input parameters to answer user questions about foam factory data.

Question: {question}

Relevant Information:
{context}

Instructions:
1. Analyze the question and the provided information.
2. Select the most appropriate ML model to answer the question. If no suitable model is found, respond with "No suitable model found."
3. Extract the necessary input parameters/variables from the question and provided information. 
4. Return the selected model name and the input parameters in JSON format. If no suitable model is found, return "No suitable model found."
5. In output, year should be number like 2025, month should be 1 to 12, factories should be 0 to 4.
6. if default values in case following are not mentioned: factories: [0], years:[2025], months:[1]
7. Strictly return output in format listed under 'Output Format:' section
6. Use this mapping:
    Factories:
        Factory 1 -> 0
        Factory 2 -> 1
        ...
        Factory 10 -> 9
7. Return model names only from this list : ["production_volume_model", "revenue_model", "profit_margin_model"]. If no model is found, return "No suitable model found."

Examples:

Question: Give production volume numbers for 2 months
Output:
{{"model_name": "production_volume_model", "input_parameters": {{"years":[2025],"months":[1, 2],"factories":[0]}}}}

Question: Give production volume  for march months
Output:
{{"model_name": "production_volume_model", "input_parameters": {{"years":[2025],"months":[3],"factories":[0]}}}}

Question: Give production volume numbers for 7 months for factory 2
Output:
{{"model_name": "production_volume_model", "input_parameters": {{"years":[2025],"months":[1, 2, 3, 4, 5, 6, 7],"factories":[1]}}}}

Question: Give production volume numbers for October for factory 4
Output:
{{"model_name": "production_volume_model", "input_parameters": {{"years":[2025],"months":[10],"factories":[3]}}}}

Question: Give profit margin numbers for October for factory 4
Output:
{{"model_name": "profit_margin_model", "input_parameters": {{"years":[2025],"months":[10],"factories":[3]}}}}

Question: Give revenue numbers for October for factory 4
Output:
{{"model_name": "revenue_model", "input_parameters": {{"years":[2025],"months":[10],"factories":[3]}}}}

**General Instructions:**

*   Select the most appropriate ML model to answer the question. If no suitable model is found, respond with "No suitable model found."
*   Extract the necessary input parameters/variables from the question and provided information. 
*   Return the selected model name and the input parameters in JSON format. If no suitable model is found, return "No suitable model found."
*   In output, year should be number like 2025, month should be 1 to 12, factories should be 0 to 4.
*   In case year(s), month(s), or factories are not mentioned in question then use following: factories: [0], years:[2025], months:[1]
*   Strictly return output in format listed under 'Output Format:' section
*   Focus on providing a clear and concise answer in natural language.
*   Handle empty results gracefully by stating that no data is available.
*   If there are multiple results, present them clearly and informatively.
*   Only use the information provided in the query results. Do not make assumptions or add extra information.

Output Format:

{{"model_name": "model_name", "input_parameters": {{"years":[year],"months":[month],"factories":[factory]}}}}

or

No suitable model found.
"""

def extract_params_from_question(question):
    """Extracts year, month, and factory from the question using regex."""
    try:
        current_year = datetime.now().year
        current_month = datetime.now().month
        years = [current_year]
        months = [current_month]
        factories = []

        year_matches = re.findall(r"\b(20\d{2})\b", question)
        if year_matches:
            years = [int(year) for year in year_matches]

        month_matches = re.findall(
            r"\b(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b",
            question, re.IGNORECASE,
        )
        if month_matches:
            month_numbers = {
                "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
                "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
                "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
                "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
            }
            months = [month_numbers[month.lower()] for month in month_matches]

        factory_matches = re.findall(r"\b(Factory [1-10])\b", question)
        if factory_matches:
            factories = factory_matches

        return {"years": years, "months": months, "factories": factories}
    except Exception as e:
        print(f"Error during parameter extraction: {e}")
        return {}

def get_model_and_params(question):
    """Retrieves the appropriate ML model and input parameters for a given question."""

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
    prompt = MODEL_SELECTION_PROMPT # Use the externally defined prompt
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

        try:
            if llm_output and len(llm_output) > 0 and "No suitable model found" in llm_output[0]:
                return None, None

            response = json.loads(llm_output[0])

            if response and "model_name" in response and "input_parameters" in response:
                final_params = response["input_parameters"]
                return response["model_name"], final_params
            else:
                print("LLM output is not in the expected JSON format:")
                print(llm_output)
                return None, None
        except (json.JSONDecodeError, IndexError, Exception) as e:
            print(f"Error processing LLM output: {str(e)}")
            print(llm_output)
            return None, None

    except Exception as e:
        print(f"Error during model and parameter retrieval: {e}")
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
    print("Output of get_model_and_params " + str(model_name)+' '+str(model_params))
    if model_name is not None:
        data = agent.run_agent(model_name, model_params)
    else:
        data = 'Unable to map model for given query!!'
    
    print("Data output final " + str(data))
    print(type(data))
    if isinstance(data, str):
        return data
    return data['output']

#Before uncommenting following call, uncomment one of the query in following function
#get_ml_answer()