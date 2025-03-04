import time
from openai import OpenAI
import streamlit as st
from streamlit_feedback import streamlit_feedback
import trubrics

from modules.kg_rag import kg_rag
from modules.kg_rag.cache import Cache

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
         /* Add left alignment */
        display: block;
        text-align: left;
        width: 100%;  /* Make buttons full width of the column */
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
    st.subheader('Ask Questions! to analyze and understand your Factories data')
    
    # Cache status and toggle
    if 'bypass_cache' not in st.session_state:
        st.session_state.bypass_cache = False
    cache_button_text = "Cache Enabled" if not st.session_state.bypass_cache else " Cache Bypassed"
    st.markdown(
        """
        <style>
            div[data-testid="stButton"] > button[kind="secondary"] {
                padding: 0.25rem 0.75rem !important;
                width: fit-content !important;
                min-width: unset !important;
                margin: 0 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.button(cache_button_text, key="cache_toggle", type="secondary"):
        st.session_state.bypass_cache = not st.session_state.bypass_cache
        st.rerun()
    
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
    st.title("Chat with Foam Factories")
    st.markdown("---")

    # Initialize session state for chat history
    if 'chat_history_bot' not in st.session_state:
        st.session_state.chat_history_bot = []
        
    # Initialize cache bypass session state if not exists
    if 'bypass_cache' not in st.session_state:
        st.session_state.bypass_cache = False
    
    

    col1, col2 = st.columns([3, 1])  # Adjust column widths here - col2 is smaller

    with col1:
        if "chat_history_bot" not in st.session_state:
            st.session_state.chat_history_bot = [
                {"role": "assistant", "content": "Hello! I'm here to help you analyze customer churn data. What would you like to know?"}
            ]
        chat_interface()


    with col2:
        st.subheader("Example Questions")
        
        examples = [
            "What is the average batch quality for each product category?",
            "What is the average batch quality for products supplied by each supplier?",
            "How does the profit margin change over time for Factory 1?",
            "Which factory had the highest total revenue in 2023?",
            "Which machines experienced defects, what was their utilization on the day of the defect?",
            "Which operators have experience greater than 7 years?",
            "Which teams operated machines that experienced defects?",
            "What is the average downtime for each machine type?"
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