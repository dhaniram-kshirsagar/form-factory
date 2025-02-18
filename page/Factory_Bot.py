import time
from openai import OpenAI
import streamlit as st
from streamlit_feedback import streamlit_feedback
import trubrics

from modules.kg_rag import kg_rag

def set_custom_css():
    st.markdown("""
    <style>
    :root {
        
    }
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, rgba(var(--primary-color-rgb), 0.1) 0%, rgba(var(--background-color-rgb), 1) 100%);
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-color);
        font-weight: 700;
        letter-spacing: -0.01em;
    }

    .stMarkdown a {
        color: var(--primary-color);
        text-decoration: none;
        border-bottom: 1px solid var(--primary-color);
        transition: opacity 0.2s ease;
    }

    .stMarkdown a:hover {
        opacity: 0.8;
    }

    .stat-card, .churner-stat-card {
        background: linear-gradient(135deg, rgba(var(--primary-color-rgb), 0.1) 0%, rgba(var(--background-color-rgb), 0.9) 100%);
        color: var(--text-color);
        border: 1px solid rgba(var(--primary-color-rgb), 0.2);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .stat-card:hover, .churner-stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }

    /* Style the subheader */
    .stMarkdown h3 {
        color: var(--primary-color);
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 20px;
    }

    /* Style code blocks in markdown */
    .stMarkdown pre {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(var(--primary-color-rgb), 0.2);
        border-radius: 10px;
        padding: 15px;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Improve readability of radio buttons */
    .stRadio > div[role="radiogroup"] > label {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(var(--primary-color-rgb), 0.2);
        padding: 12px 15px;
        border-radius: 8px;
        margin-bottom: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .stRadio > div[role="radiogroup"] > label:hover {
        background-color: rgba(var(--primary-color-rgb), 0.05);
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
    }

    .stRadio > div[role="radiogroup"] > label[data-checked="true"] {
        background-color: rgba(var(--primary-color-rgb), 0.1);
        border-color: var(--primary-color);
        font-weight: 500;
    }

    /* Style buttons */
    .stButton > button {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
    }

    /* Style text inputs */
    .stTextInput > div > div > input {
        border-radius: 8px;
        padding: 10px 15px;
        border: 1px solid rgba(var(--primary-color-rgb), 0.2);
        background-color: var(--background-color);
        color: var(--text-color);
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(var(--primary-color-rgb), 0.2);
    }

    /* Style selectbox */
    .stSelectbox > div > div > div {
        border-radius: 8px;
        border: 1px solid rgba(var(--primary-color-rgb), 0.2);
        background-color: var(--background-color);
    }

    /* Improve overall spacing */
    .stMarkdown {
        line-height: 1.6;
        margin-bottom: 20px;
    }

    .stMarkdown p {
        margin-bottom: 15px;
    }

    </style>
    """, unsafe_allow_html=True)

# Chatbot function
def chatbot(query):
    time.sleep(1)  # Simulate a longer processing time
    return  kg_rag.get_kg_answer(query)

# Chat interface
def chat_interface():
    st.subheader('Ask Questions! to analyze and understand your churn data')
    if prompt := st.chat_input(placeholder='Hello! I am here to help. What would you like to know?'):
        if prompt:
            with st.spinner("Analyzing data... ⏳"): # Added hourglass emoji
                response = chatbot(prompt)
            st.session_state.chat_history_bot.append(('You', prompt))
            st.session_state.chat_history_bot.append(('Bot', response['result']))
    
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container"><h5>Chat History</h5>', unsafe_allow_html=True)
        # Display message pairs in reverse order
        for i in range(len(st.session_state.chat_history_bot)-1, -1, -2):
            if i-1 >= 0:
                bot_role, bot_msg = st.session_state.chat_history_bot[i-1]
                with st.chat_message("assistant"):
                    st.markdown(f'<div class="chat-message {bot_role.lower()}"><strong>{bot_role}</strong>: {bot_msg}</div>', unsafe_allow_html=True)
            if i >= 0:
                user_role, user_msg = st.session_state.chat_history_bot[i]
                with st.chat_message("user"):
                    st.markdown(f'<div class="chat-message {user_role.lower()}"><strong>{user_role}</strong>: {user_msg}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_factorybot():
    set_custom_css()
    st.title("Churn Analysis ChatBot")
    st.markdown("---")

     # Initialize session state for chat history
    if 'chat_history_bot' not in st.session_state:
        st.session_state.chat_history_bot = []

    col1, col2 = st.columns([2, 1])  # Adjust column widths here

    with col1:
        if "chat_history_bot" not in st.session_state:
            st.session_state.chat_history_bot = [
                {"role": "assistant", "content": "Hello! I'm here to help you analyze customer churn data. What would you like to know?"}
            ]
        chat_interface()
        '''# Initialize session state variables
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm here to help you analyze customer churn data. What would you like to know?"}
            ]

        if "response" not in st.session_state:
            st.session_state["response"] = None

        if "waiting_for_response" not in st.session_state:
            st.session_state.waiting_for_response = False

        if "last_user_message" not in st.session_state:
            st.session_state.last_user_message = None

        # Show bot's initial message
        if len(st.session_state.messages) == 1:
            st.chat_message("assistant").write(st.session_state.messages[0]["content"])

        # Chat input
        if prompt := st.chat_input(placeholder="Ask a question about customer churn...", disabled=st.session_state.waiting_for_response) or st.session_state.waiting_for_response:
            if not st.session_state.waiting_for_response:
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.last_user_message = prompt
                st.session_state.waiting_for_response = True
                st.rerun()
            else:
                with st.spinner("Analyzing data..."):
                    time.sleep(1)
                    print(prompt)
                    st.session_state["response"] = kg_rag.get_kg_answer(st.session_state.last_user_message)
                    st.session_state.messages.append({"role": "assistant", "content": st.session_state["response"]})
                    st.session_state.waiting_for_response = False
                    st.rerun()

        # Display all messages except initial bot message
        messages = st.session_state.messages[1:]
        for i in range(len(messages)):
            msg = messages[i]
            st.chat_message(msg["role"]).write(msg["content"])'''
        

    with col2:
        st.subheader("Example Questions")
        markdown = """
        You can start with the following examples:

        1. How does the tenure of customers correlate with their service usage?
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
        16. Identify customers who have churned and have a lower tenure than the average tenure of all customers.
        """
        examples = [
            "How does the tenure of customers correlate with their service usage?",
            "Is there a significant difference in churn rates based on payment methods?",
            "How does the presence of online security, backup, and tech support services affect customer satisfaction and churn?",
            "What payment methods are most commonly used by customers?",
            "Identify customers who have churned, have fiber optic internet service, and have not subscribed to any streaming services.",
            "Find customers who have churned, have a low tenure (e.g., less than 2 years), and have not opted for paperless billing.",
            "Identify customers who have churned, have a high monthly charge (e.g., above $80), and have a low tenure (e.g., less than 2 years).",
            "Find customers who have churned, have fiber optic internet service, and have not opted for tech support or online security.",
            "Identify the top 5 services most frequently used by churned customers.",
            "Retrieve customers who have a 'Month-to-month' contract.",
            "Calculate the churn rate for customers with 'Month-to-month' contracts.",
            "Find customers who have churned and have a higher monthly charge than the average monthly charge of all customers.",
            "Identify customers who have churned and have a lower tenure than the average tenure of all customers.",
            "Find customers who have churned and have the least common combination of internet service and streaming services.",
            "Which factors are most strongly associated with customer churn (e.g., monthly charges, tenure, contract type)?",
            "Identify customers who have churned and have a lower tenure than the average tenure of all customers."
        ]

        for i, example in enumerate(examples):
            if st.button(example, key=f"example_{i}"):
                # Call the chatbot function and display the response
                with st.spinner("Analyzing data... ⏳"):
                    response = chatbot(example)
                # Update the chat history
                st.session_state.chat_history_bot.append(('You', example))
                st.session_state.chat_history_bot.append(('Bot', response['result']))
                # Rerun the app to display the updated chat history
                st.rerun()

# Commented out feedback section
# if st.session_state["response"]:
#     feedback = streamlit_feedback(
#         feedback_type="thumbs",
#         optional_text_label="[Optional] Please provide an explanation",
#         key=f"feedback_{len(messages)}",
#     )
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