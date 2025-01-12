import time
from openai import OpenAI
import streamlit as st
from streamlit_feedback import streamlit_feedback
import trubrics

from modules.kg_rag import kg_rag

kg_rag.init_graph()

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="feedback_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/5_Chat_with_user_feedback.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

def show_factorybot():
    st.subheader(":robot_face: Chat with Foam Factories")
    
    #st.set_page_config(layout="wide")

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

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I help you? Leave feedback to help me improve!"}
        ]

    if "response" not in st.session_state:
        st.session_state["response"] = None

    if "waiting_for_response" not in st.session_state:
        st.session_state.waiting_for_response = False

    messages = st.session_state.messages
    for msg in messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="e.g. List factories which are having low production vlume.", disabled=st.session_state.waiting_for_response) or st.session_state.waiting_for_response:
        if not st.session_state.waiting_for_response:
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.last_user_message = prompt
            st.chat_message("user").write(prompt)
            st.session_state.waiting_for_response = True
            st.rerun()
        else:
            with st.spinner("Assistant is typing..."):
                time.sleep(1)
                print(prompt)
                st.session_state["response"] = kg_rag.get_kg_answer(st.session_state.last_user_message)
                with st.chat_message("assistant"):
                    st.session_state.messages.append({"role": "assistant", "content": st.session_state["response"]})
                    st.write(st.session_state["response"])
                st.session_state.waiting_for_response = False
                st.rerun()

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