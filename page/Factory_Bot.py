import time
from openai import OpenAI
import streamlit as st
from streamlit_feedback import streamlit_feedback
import trubrics

from modules.kg_rag import kg_rag

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="feedback_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/5_Chat_with_user_feedback.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

def show_factorybot():
    st.subheader(":robot_face: Get insights from your churn data")

    
    markdown = """
    You can start with following examples:

        1. How does the tenure of customers correlate with their service usage?-
        2. Is there a significant difference in churn rates based on payment methods?
        3. How does the presence of online security, backup, and tech support services affect customer satisfaction and churn?
        4. What payment methods are most commonly used by customers?
        5. Identify customers who have churned, have fiber optic internet service, and have not subscribed to any streaming services.
        6. Find customers who have churned, have a low tenure (e.g., less than 2 years), and have not opted for paperless billing.
        7. Identify customers who have churned, have a high monthly charge (e.g., above $80), and have a low tenure (e.g., less than 2 years).
        8. Find customers who have churned, have fiber optic internet service, and have not opted for tech support or online security.
        9. Identify the top 5 services most frequently used by churned customers.
        10. Retrieve customers who have a "Month-to-month" contract.
        11. Calculate the churn rate for customers with "Month-to-month" contracts.
        12. Find customers who have churned and have a higher monthly charge than the average monthly charge of all customers.
        13. Identify customers who have churned and have a lower tenure than the average tenure of all customers.
        14. Find customers who have churned and have the least common combination of internet service and streaming services.
        15. Which factors are most strongly associated with customer churn (e.g., monthly charges, tenure, contract type)?

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