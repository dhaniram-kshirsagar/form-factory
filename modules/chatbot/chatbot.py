import streamlit as st
import pandas as pd
import os
from pathlib import Path



import openai
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

from modules.kg_rag import kg_rag

@st.dialog("Foam Factory Robo Chat")
def open_chatbot():
    openai.api_key = os.environ["OPENAI_API_KEY"]

    if "messages" not in st.session_state.keys():  # Initialize the chat messages history
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Ask me a question about Foam Factories!",
            }
        ]

    #index = load_data()

    # if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    #     st.session_state.chat_engine = index.as_chat_engine(
    #         chat_mode="condense_question", verbose=True, streaming=True
    #     )

    if prompt := st.chat_input(
        "Ask a question"
    ):  # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:  # Write message history to UI
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            response_stream = kg_rag.get_kg_answer(prompt)
            st.write_stream(response_stream)
            message = {"role": "assistant", "content": response_stream}
            # Add response to message history
            st.session_state.messages.append(message)


from modules.data import data as d

@st.cache_resource(show_spinner=False)
def load_data():
    docs = d.load_data_for_llm()
    Settings.llm = OpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2,
        system_prompt="""You are an expert on 
        the foam factories performance data and maintenance questions. 
        Assume that all questions are related 
        to the foam factories performance and maintenance. Keep 
        your answers technical and based on 
        facts – do not hallucinate features.""",
    )
    index = VectorStoreIndex.from_documents(docs)
    return index
