import os
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
import json

print('Initializing vectory db for ML model RAG...')

from pathlib import Path

#MODEL_DESCRTIPTIONS_FILE = '/workspaces/form-factory/modules/ml/'+"model_descriptions.json"
MODEL_DESCRTIPTIONS_FILE = Path(__file__).parent.parent/"ml/model_descriptions.json"

#DATA_DESCRIPTION_FILE = '/workspaces/form-factory/modules/ml/'+"data_descriptions.json"
DATA_DESCRIPTION_FILE = Path(__file__).parent.parent/"ml/data_descriptions.json"

# --- Configuration ---
#VECTOR_DB_PATH = '/workspaces/form-factory/modules/ml/'+"factory_vector_db"
VECTOR_DB_PATH = Path(__file__).parent.parent/"ml/factory_vector_db"

EMBEDDINGS_MODEL = "all-mpnet-base-v2" # or any other Sentence Transformer model

# 1. Load Data Descriptions
try:
    with open(DATA_DESCRIPTION_FILE, 'r') as f:
        data_descriptions = json.load(f)
except FileNotFoundError:
    print(f"Error: {DATA_DESCRIPTION_FILE} not found. Create this file.")
    exit()

# 2. Load Model Descriptions
try:
    with open(MODEL_DESCRTIPTIONS_FILE, 'r') as f:
        model_descriptions = json.load(f)
except FileNotFoundError:
    print(f"Error: {MODEL_DESCRTIPTIONS_FILE} not found. Create this file.")
    exit()

# 3. Create Documents for Vector Database
documents = []

# Model Descriptions
for model_name, model_data in model_descriptions.items():
    text = f"Model Name: {model_name}\nTarget Variable: {model_data['target_variable']}\nInput Features: {', '.join(model_data['input_features'])}\nDescription: {model_data.get('description', 'No description provided.')}"
    metadata = {"type": "model", "model_name": model_name, **model_data}
    documents.append({"page_content": text, "metadata": metadata})

# Data Descriptions
for df_name, df_data in data_descriptions.items():
    for col_name, col_data in df_data.items():
        text = f"DataFrame: {df_name}\nColumn: {col_name}\nData Type: {col_data['data_type']}\nDescription: {col_data.get('description', 'No description provided.')}"
        metadata = {"type": "data", "dataframe_name": df_name, "column_name": col_name, **col_data}
        documents.append({"page_content": text, "metadata": metadata})


# Example questions (optional - you can add more)
example_questions = [
    {"question": "What will be the production volume next week for factory 1?", "model_name": "production_model", "input_features": ["date", "factory_id"]},
    {"question": "Predict the profit margin if market demand is high and production volume is 1500.", "model_name": "profit_model", "input_features": ["market_demand", "production_volume"]},
        {"question": "How many breakdowns can be predicted on 2024-01-01 for machine A", "model_name": "breakdown_model", "input_features": ["date", "machine_id"]}

]

for example in example_questions:
    text = f"Question: {example['question']}\nModel: {example['model_name']}\nInput Features: {', '.join(example['input_features'])}"
    metadata = {"type": "example", **example}
    documents.append({"page_content": text, "metadata": metadata})

# 4. Create Embeddings and Vector Database
embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDINGS_MODEL)

# Convert list of dict to list of Document objects
from langchain.docstore.document import Document
docs = [Document(**d) for d in documents]

# Create vector database or load existing one
if os.path.exists(VECTOR_DB_PATH):
    vector_db = FAISS.load_local(VECTOR_DB_PATH, embeddings)
    print("Loaded existing vector database.")
else:
    vector_db = FAISS.from_documents(docs, embeddings)
    vector_db.save_local(VECTOR_DB_PATH)
    print("Created and saved new vector database.")

# def get_context(query):
#     docs = vector_db.similarity_search(query)

#     print("\nRetrieved Documents:")
#     for doc in docs:
#         print(doc.page_content)
#         print(doc.metadata)
#         print("-" * 20)
    
#     return docs