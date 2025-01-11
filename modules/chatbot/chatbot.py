import streamlit as st
import os

import openai
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
            response_stream = kg_rag.yeild_kg_answer(prompt)
            st.write_stream(response_stream)
            message = {"role": "assistant", "content": response_stream}
            # Add response to message history
            st.session_state.messages.append(message)


