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
    st.subheader(":robot_face: Chat with Foam Factories")
    
    # Define the content for each column
    column_1_content = """
        ### Examples of questions you can ask:
    ##### 1. **Quality Analysis**
     - **Average Quality:**
        - What is the average batch quality for each product category?
        - What is the average batch quality for products supplied by each supplier?
    ##### 2. **Profitability & Revenue**
     - **Profit Margin**:
        - How does the profit margin change over time for Factory 1?
     - **Revenue Comparison**:
        - Which factory had the highest total revenue in 2023?
   """

    column_2_content = """
    #####
    ##### 3. **Defects & Operators**
    - **Defect Analysis:**
        - Which machines experienced defects caused by 'Material Impurity', and what was their utilization on the day of the defect?
     - **Operator Experience:**
        - Which operators have experience greater than 7 years?
        - Which operators operated machines that experienced defects?
    ##### 4. **Efficiency & Downtime**
    -  **Downtime Analysis**:
         - What is the average downtime for each machine type?"""

    # Create two columns
    col1, col2 = st.columns(2)

    # Render the content in the respective columns
    with col1:
        st.markdown(column_1_content)

    with col2:
        st.markdown(column_2_content)



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
                llmresp = kg_rag.get_kg_answer(st.session_state.last_user_message)
                print(llmresp)
                st.session_state["response"] = llmresp['result']
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