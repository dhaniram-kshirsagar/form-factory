import streamlit as st
from openai import OpenAI
import streamlit as st
from streamlit_feedback import streamlit_feedback
import trubrics

from modules.ml import ml_rag


# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="feedback_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/5_Chat_with_user_feedback.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("📝 Predict Factory Performance with Factory Astro")
#st.set_page_config(layout="wide")

markdown = """
You can start with following examples:

    - What will revenue for factor 3 next year?
    - What will be form density like in July for factor 2?
    - What will be production volume over next 2 months?
    - What will be foam density of factory 1 in city A?
    - What will be revenue over next 2 months for factory 3 in city c?
    - Get me production volume for factor 4 city c in month of July

"""

st.markdown(markdown)

if "astro_messages" not in st.session_state:
    st.session_state.astro_messages = [
        {"role": "assistant", "content": "How can I help you? Leave feedback to help me improve!"}
    ]
if "response" not in st.session_state:
    st.session_state["astro_response"] = None

messages = st.session_state.astro_messages
for msg in messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="e.g. Get me production volume for factor 4 city c in month of July."):
    st.session_state.astro_messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    st.session_state["astro_response"] = ml_rag.get_ml_answer(prompt)
    with st.chat_message("assistant"):
        st.session_state.astro_messages.append({"role": "assistant", "content": st.session_state["astro_response"]})
        st.write(st.session_state["astro_response"])

st.markdown('NOTE Its work in progress... In the generated output: Add +1 to Factory name. Assume City A if "location 0", City B if "location 1" and so on.. We are working to map factory and location names.')
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