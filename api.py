from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict
import uvicorn
from datetime import datetime, timedelta

import os
import streamlit as st
from modules.kg_rag import kg_rag, q_engine

API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

from pydantic import BaseModel


class Base(BaseModel):
    message: str

# API routes
@app.post("/chat")
async def chat_with_data(chat_input: Base):
    print(f'Recieved message: {chat_input.message}')
    return kg_rag.get_kg_answer(chat_input.message)

@app.post("/cquery")
async def chat_with_data(chat_input: Base):
    print(f'Recieved message: {chat_input.message}')
    return q_engine.execute_query(chat_input.message)

def run_api_server():
    print("Begin to start the API server")
    if not hasattr(st, 'already_started_server'):
    # Hack the fact that Python modules (like st) only load once to
    # keep track of whether this file already ran.
        st.already_started_server = True
        uvicorn.run(app, host=API_HOST, port=API_PORT)
        print("Successfully start the API server")
    else:
        print("API server already started!!")
