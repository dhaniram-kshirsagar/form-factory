from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import json

from modules.ml import vector_store as vs
from modules.ml import agent

# Configuration
VECTOR_DB_PATH = "factory_vector_db"
EMBEDDINGS_MODEL = "all-mpnet-base-v2"
LLM_MODEL = "gpt-3.5-turbo" # or gpt-4
MODEL_SELECTION_PROMPT = """
You are an expert system designed to select the best machine learning model and extract input parameters to answer user questions about factory data.

Question: {question}

Relevant Information:
{context}

Instructions:
1. Analyze the question and the provided information.
2. Select the most appropriate ML model to answer the question. If no suitable model is found, respond with "No suitable model found."
3. Extract the necessary input parameters/variables from the question and provided information. If no input parameters are needed or can be found, return empty list.
4. Return the selected model name and the input parameters in JSON format. If no suitable model is found, return "No suitable model found."

Output Format:
```json
{{"model_name": "model_name", "input_parameters": ["param1", "param2", ...]}}
or

No suitable model found.
"""

def get_model_and_params(question):
    """Retrieves the appropriate ML model and input parameters for a given question."""

    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDINGS_MODEL)
    vector_db = FAISS.load_local(VECTOR_DB_PATH, embeddings)

    # Retrieval
    docs = vector_db.similarity_search(question, k=5) # Retrieve top 5 relevant documents
    context = "\n".join([doc.page_content for doc in docs])

    # Prompt Engineering
    prompt = PromptTemplate(
        input_variables=["question", "context"],
        template=MODEL_SELECTION_PROMPT,
    )
    final_prompt = prompt.format(question=question, context=context)

    # LLM Call
    llm = OpenAI(temperature=0, model=LLM_MODEL) # Set temperature to 0 for deterministic output.
    llm_output = llm(final_prompt)

    try:
        # Attempt to parse the LLM output as JSON
        response = json.loads(llm_output)

        if "model_name" in response and "input_parameters" in response:
            return response["model_name"], response["input_parameters"]
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
    agent.run_agent(model_name, model_params)