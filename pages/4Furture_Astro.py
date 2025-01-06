from openai import OpenAI
import streamlit as st
from streamlit_feedback import streamlit_feedback
import trubrics

from modules.kg_rag import kg_rag

st.set_page_config(layout="wide")
# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="feedback_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/5_Chat_with_user_feedback.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("📝 Chat with Furture Astro")


markdown = """
You can start with following examples:

    - What is the average batch quality for each product category?
    - How does the profit margin change over time for Factory 1?
    - For each factory, what is the total production volume and the average profit margin on days when the production volume was above the average production volume for that factory?
    - Which machines experienced defects caused by 'Material Impurity' and what was their utilization on the day of the defect?
    - Which operators have experience greater than 7 years and operated machines that experienced defects?
    - What is the average batch quality for products supplied by each supplier?
    - What is the average downtime for each machine type?
    - Which factory had the highest total revenue in 2023?
    - How does the co2 emissions change over time for machine "City A-1-Type A" in year 2023?
    - What is the total energy consumption for each factory in 2023?
"""

st.markdown(markdown)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you? Leave feedback to help me improve!"}
    ]
if "response" not in st.session_state:
    st.session_state["response"] = None
if "location" not in st.session_state:
    st.session_state["location"] = None


# Location selection in top bar (using container to better center it)
locations = ["Location 1", "Location 2", "Location 3", "Location 4"]  # selcet the Location
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_location = st.selectbox("Select a Location for Prediction", locations, key="location_select_top")
        st.session_state.location = selected_location

# Display selected location
if st.session_state.location:
    st.write(f"Selected Location: {st.session_state.location}")


# Display Chat Messages
messages = st.session_state.messages
for msg in messages:
    st.chat_message(msg["role"]).write(msg["content"])


# Chat input and processing
if prompt := st.chat_input(placeholder="e.g. List factories which are having low production vlume."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Modify the prompt to include location before making the prediction
    if st.session_state.location:
        prompt_with_location = f"Regarding location: {st.session_state.location}, {prompt}"
        st.session_state["response"] = kg_rag.get_kg_answer(prompt_with_location)
    else:
        st.session_state["response"] = kg_rag.get_kg_answer(prompt)

    with st.chat_message("assistant"):
        st.session_state.messages.append({"role": "assistant", "content": st.session_state["response"]})
        st.write(st.session_state["response"])

# Feedback Section (Commented out for clarity - uncomment if needed)
# if st.session_state["response"]:
#     feedback = streamlit_feedback(
#         feedback_type="thumbs",
#         optional_text_label="[Optional] Please provide an explanation",
#         key=f"feedback_{len(messages)}",
#     )
#     # This app is logging feedback to Trubrics backend, but you can send it anywhere.
#     # The return value of streamlit_feedback() is just a dict.
#     # Configure your own account at https://trubrics.streamlit.app/
#     if feedback and "TRUBRICS_EMAIL" in st.secrets:
#         config = trubrics.init(
#             email=st.secrets.TRUBRICS_EMAIL,
#             password=st.secrets.TRUBRICS_PASSWORD,
#         )
#         collection = trubrics.collect(
#             component_name="default",
#             model="gpt",
#             response=feedback,
#             metadata={"chat": messages},
#         )
#         trubrics.save(config, collection)
#         st.toast("Feedback recorded!", icon="📝")