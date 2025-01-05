import json
import re
from datetime import datetime

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

import os

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = ""

# --- Configuration ---
VECTOR_DB_PATH = "factory_vector_db"
EMBEDDINGS_MODEL = "all-mpnet-base-v2"
LLM_MODEL = "gpt-3.5-turbo"

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

Output Format:
```json

{{"model_name": "model_name", "input_parameters": {{"years":year,"months":month,"factories":factory,"locations":location}}}}

or

No suitable model found.
"""

def extract_params_from_question(question):
    """Extracts year, month, factory, and location from the question using regex."""
    try:
        current_year = datetime.now().year
        current_month = datetime.now().month
        years = [current_year]
        months = [current_month]
        factories = []
        locations = []

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

        location_matches = re.findall(r"\b(City [A-E])\b", question)
        if location_matches:
            locations = location_matches

        return {"years": years, "months": months, "factories": factories, "locations": locations}
    except Exception as e:
        print(f"Error during parameter extraction: {e}")
        return {}


def get_model_and_params(question):
    """Retrieves the appropriate ML model and input parameters for a given question."""

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)
    try:
        vector_db = FAISS.load_local('/workspaces/form-factory/modules/ml/'+VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
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

    # LLM Call
    llm = ChatOpenAI(temperature=0, model=LLM_MODEL)

    try:
        messages = [HumanMessage(content=final_prompt)] # Create a list of messages
        llm_output = llm.invoke(messages).content
        response = json.loads(llm_output)
        if "model_name" in response and "input_parameters" in response:
            extracted_params = extract_params_from_question(question)
            final_params = response["input_parameters"]
            for key in extracted_params:
                if extracted_params[key]:
                    final_params[key] = extracted_params[key]
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
        
def main():
    query = "What will be production volume over next 6 months?"
    model_name, model_params = get_model_and_params(query)
    print(model_name)
    print(model_params)
    #agent.run_agent(model_name, model_params)

main()