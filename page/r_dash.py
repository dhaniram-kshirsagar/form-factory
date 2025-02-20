import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from streamlit_option_menu import option_menu  # Import streamlit_option_menu

from modules.kg_rag import kg_rag

CHURN_DATA_FILE = Path(__file__).parent.parent / "modules/data/telchurn/TelecomChurn.csv"

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(CHURN_DATA_FILE)  # Replace with your actual CSV file path
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    #df = df.dropna()  # Drop rows with NaN values
    df['SeniorCitizen'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})
    return df

# Custom CSS
def set_custom_css():
    st.markdown("""
    <style>
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

    .stat-card, .churner-stat-card, .key-insight-card {
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .stat-card {
        background: #e6f3ff;
        color: #DE3163;
        border: 1px solid rgba(var(--primary-color-rgb), 0.2);
        padding: 5px;
        border-radius: 5px;
        margin-bottom: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }

    .churner-stat-card {
        background: #ffe6e6;
        color: #660000;
        border: 1px solid rgba(var(--primary-color-rgb), 0.2);
        padding: 5px;
        border-radius: 5px;
        margin-bottom: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .churner-stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }

    .key-insight-card {
        background: #e6ffe6;
        color: #006600;
        border: 1px solid rgba(var(--primary-color-rgb), 0.2);
        padding: 5px;
        border-radius: 5px;
        margin-bottom: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .key-insight-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }

    .stMarkdown h3 {
        color: var(--primary-color);
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 20px;
    }

    .stMarkdown pre {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(var(--primary-color-rgb), 0.2);
        border-radius: 10px;
        padding: 15px;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }

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

    .stSelectbox > div > div > div {
        border-radius: 8px;
        border: 1px solid rgba(var(--primary-color-rgb), 0.2);
        background-color: var(--background-color);
    }

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
    # response = generateText({
    #     "model": openai("gpt-4o"),
    #     "prompt": f"You are a helpful assistant for a telecom customer churn analysis dashboard. Answer the following question: {query}"
    # })
    #return response.text
    return  kg_rag.get_kg_answer(query)

# Chat interface
def chat_interface():
    st.subheader('Ask Questions! churn insights')
    if prompt := st.chat_input(placeholder='e.g. What is the churn for customer using DSL?'):
        if prompt:
            response = chatbot(prompt)
            st.session_state.chat_history.append(('You', prompt))
            st.session_state.chat_history.append(('Bot', response['result']))

    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container"><h5>Chat History</h5>', unsafe_allow_html=True)
        # Display message pairs in reverse order
        for i in range(len(st.session_state.chat_history)-1, -1, -2):
            if i-1 >= 0:
                bot_role, bot_msg = st.session_state.chat_history[i-1]
                with st.chat_message("assistant"):
                    st.markdown(f'<div class="chat-message {bot_role.lower()}"><strong>{bot_role}</strong>: {bot_msg}</div>', unsafe_allow_html=True)
            if i >= 0:
                user_role, user_msg = st.session_state.chat_history[i]
                with st.chat_message("user"):
                    st.markdown(f'<div class="chat-message {user_role.lower()}"><strong>{user_role}</strong>: {user_msg}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Helper function to create donut charts
def create_donut_chart(data, column, title, colors):
    value_counts = data[column].value_counts()
    fig = go.Figure(data=[go.Pie(labels=value_counts.index, values=value_counts.values, hole=.6, marker_colors=colors)])
    fig.update_layout(
        title_text=title,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        annotations=[dict(text=f'{len(data)}', x=0.5, y=0.5, font_size=20, showarrow=False)],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig

# Helper function to create progress bars
def create_progress_bars(data, column):
    value_counts = data[column].value_counts().sort_index()
    max_value = value_counts.max()
    for label, value in value_counts.items():
        progress = st.progress(0)
        progress.progress(int(value / max_value * 100))
        st.write(f"{label}: {value}")

# Function to create a small donut chart using Plotly
def create_small_donut_chart(data, values, names, title):
    fig = go.Figure(data=[go.Pie(labels=names, values=values, hole=.6)])
    fig.update_layout(
        title_text=title,
        showlegend=False,
        height=200,
        width=200,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig

# Function to create an enhanced stat box
def create_enhanced_stat_box(title, icon, value, subvalue):
    return f"""
    <div class="enhanced-stat-box">
        <div class="enhanced-stat-header">
            <div class="enhanced-stat-icon">{icon}</div>
            <div class="enhanced-stat-title">{title}</div>
        </div>
        <div class="enhanced-stat-content">
            <div class="enhanced-stat-text">
                <div class="enhanced-stat-value">{value}</div>
                <div class="enhanced-stat-subvalue">{subvalue}</div>
            </div>
        </div>
    </div>
    """

# Main function
def show_r_dash():

    df = load_data()

    set_custom_css()

    st.title("TELECOM CUSTOMER CHURN ANALYSIS")

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Create two columns: one for navigation and chat, one for content
    left_col, content_col = st.columns([1.5, 2.5])

    # Navigation and chat interface in the left column
    with left_col:
        #st.title("TELECOM CUSTOMER CHURN ANALYSIS")
        selected = option_menu(
            "Profile Menu",
            ["Summary", "Customer Profile", "Churner Profile"],
            icons=['house', 'person', 'exclamation-triangle'],
            menu_icon="cast", default_index=0,
            styles={
                "container": {"padding": "45px 10px!important", "background-color": "transparent"},
                "icon": {"color": "var(--primary-color)", "font-size": "20px"}, 
                "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "rgba(255, 255, 255, 0.1)"},
                "nav-link-selected": {"background-color": "var(--primary-color)", "color": "white"},
            }
        )

        st.markdown("---")
        chat_interface()

    # Main content in the right column
    with content_col:
        if selected == "Summary":
            summary_page(df)
        elif selected == "Customer Profile":
            customer_profile_page(df)
        elif selected == "Churner Profile":
            churner_profile_page(df)

# Summary page
def summary_page(df):
    st.title("SUMMARY")

    churners = df[df['Churn'] == 'Yes']
    non_churners = df[df['Churn'] == 'No']

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="stat-card"><h4>Customer Profile Overview</h4></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-card">Total Customers <br><h2> {len(df)}</h2></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-card">Avg Monthly Charge <br><h2> ${df["MonthlyCharges"].mean():.2f}</h2></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-card">Avg Total Charge <br><h2> ${df["TotalCharges"].mean():.2f}</h2></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="churner-stat-card"><h4>Churner Profile Overview</h4></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="churner-stat-card">Total Churners <br><h2> {len(churners)}</h2></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="churner-stat-card">Avg Monthly Charge <br><h2> ${churners["MonthlyCharges"].mean():.2f}</h2></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="churner-stat-card">Avg Total Charge <br><h2> ${churners["TotalCharges"].mean():.2f}</h2></div>', unsafe_allow_html=True)

    st.subheader("Key Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="key-insight-card">
            <div class="key-insight-icon">📊</div>
            <div class="key-insight-content">
                <div class="key-insight-title">Churn Rate</div>
                <div class="key-insight-value">{len(churners) / len(df):.2%}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="key-insight-card">
            <div class="key-insight-icon">📅</div>
            <div class="key-insight-content">
                <div class="key-insight-title">Avg Tenure (Churners)</div>
                <div class="key-insight-value">{churners['tenure'].mean():.2f} months</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="key-insight-card">
            <div class="key-insight-icon">📅</div>
            <div class="key-insight-content">
                <div class="key-insight-title">Avg Tenure (Non-churners)</div>
                <div class="key-insight-value">{non_churners['tenure'].mean():.2f} months</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="key-insight-card">
            <div class="key-insight-icon">📑</div>
            <div class="key-insight-content">
                <div class="key-insight-title">Most Common Contract (Churners)</div>
                <div class="key-insight-value">{churners['Contract'].mode().values[0]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="key-insight-card">
        <div class="key-insight-icon">🌐</div>
        <div class="key-insight-content">
            <div class="key-insight-title">Most Common Internet Service (Churners)</div>
            <div class="key-insight-value">{churners['InternetService'].mode().values[0]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Customer Profile page
def customer_profile_page(df):
    st.title("CUSTOMER PROFILE")
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        st.markdown(f'<div class="stat-card">TOTAL CUSTOMERS<br><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card">MONTHLY CHARGE (AVG)<br><h2>${df["MonthlyCharges"].mean():.2f}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card">TOTAL CHARGE (AVG)<br><h2>${df["TotalCharges"].mean():.2f}</h2></div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.plotly_chart(create_donut_chart(df, 'gender', "GENDER", ['#1e90ff', '#0047ab']), use_container_width=True)

    with col2:
        st.markdown('<div class="stat-card">TENURE</div>', unsafe_allow_html=True)
        df['tenure_group'] = pd.cut(df['tenure'], bins=[0, 12, 24, 36, 48, 60, float('inf')], labels=['0-12', '13-24', '25-36', '37-48', '49-60', '60+'])
        create_progress_bars(df, 'tenure_group')

    with col3:
        st.plotly_chart(create_donut_chart(df, 'InternetService', "INTERNET SERVICE", ['#1e90ff', '#4169e1', '#0047ab']), use_container_width=True)

    with col4:
        st.plotly_chart(create_donut_chart(df, 'Contract', "CONTRACT", ['#1e90ff', '#4169e1', '#0047ab']), use_container_width=True)

    st.subheader("ADDITIONAL STATS")

    col1, col2 = st.columns(2)

    # Senior Citizens
    senior_citizens = df['SeniorCitizen'].value_counts()
    with col1:
        st.markdown(create_enhanced_stat_box(
            "Senior Citizens",
            "👴",
            f"{senior_citizens.get('Yes', 0)}",
            f"{senior_citizens.get('Yes', 0) / len(df):.1%} of customers"
        ), unsafe_allow_html=True)
        st.plotly_chart(create_small_donut_chart(df, senior_citizens.values, senior_citizens.index, "Senior Citizens"), use_container_width=True)

    # Customers with Partners
    partner_counts = df['Partner'].value_counts()
    with col2:
        st.markdown(create_enhanced_stat_box(
            "Customers with Partners",
            "👫",
            f"{partner_counts.get('Yes', 0)}",
            f"{partner_counts.get('Yes', 0) / len(df):.1%} of customers"
        ), unsafe_allow_html=True)
        st.plotly_chart(create_small_donut_chart(df, partner_counts.values, partner_counts.index, "Customers with Partners"), use_container_width=True)

    # Phone Service Subscribers
    phone_service_counts = df['PhoneService'].value_counts()
    with col1:
        st.markdown(create_enhanced_stat_box(
            "Phone Service Subscribers",
            "📞",
            f"{phone_service_counts.get('Yes', 0)}",
            f"{phone_service_counts.get('Yes', 0) / len(df):.1%} of customers"
        ), unsafe_allow_html=True)
        st.plotly_chart(create_small_donut_chart(df, phone_service_counts.values, phone_service_counts.index, "Phone Service Subscribers"), use_container_width=True)

    # Payment Methods
    payment_methods = df['PaymentMethod'].value_counts()
    with col2:
        st.markdown(create_enhanced_stat_box(
            "Payment Methods",
            "💳",
            f"{len(payment_methods)} types",
            f"Most common: {payment_methods.index[0]}"
        ), unsafe_allow_html=True)
        st.plotly_chart(create_small_donut_chart(df, payment_methods.values, payment_methods.index, "Payment Methods"), use_container_width=True)

# Churner Profile page
def churner_profile_page(df):
    churners = df[df['Churn'] == 'Yes']
    st.title("CHURNER PROFILE")
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        st.markdown(f'<div class="churner-stat-card">TOTAL CHURNERS<br><h2>{len(churners)}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="churner-stat-card">MONTHLY CHARGE (AVG)<br><h2>${churners["MonthlyCharges"].mean():.2f}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="churner-stat-card">TOTAL CHARGE (AVG)<br><h2>${churners["TotalCharges"].mean():.2f}</h2></div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.plotly_chart(create_donut_chart(churners, 'gender', "GENDER", ['#ff6b6b', '#ff4444']), use_container_width=True)

    with col2:
        st.markdown('<div class="churner-stat-card">TENURE</div>', unsafe_allow_html=True)
        churners['tenure_group'] = pd.cut(churners['tenure'], bins=[0, 12, 24, 36, 48, 60, float('inf')], labels=['0-12', '13-24', '25-36', '37-48', '49-60', '60+'])
        create_progress_bars(churners, 'tenure_group')

    with col3:
        st.plotly_chart(create_donut_chart(churners, 'InternetService', "INTERNET SERVICE", ['#ff4444', '#ff6b6b', '#ff8888']), use_container_width=True)

    with col4:
        st.plotly_chart(create_donut_chart(churners, 'Contract', "CONTRACT", ['#ff4444', '#ff6b6b', '#ff8888']), use_container_width=True)

    st.subheader("ADDITIONAL STATS")

    col1, col2 = st.columns(2)

    # Senior Citizen Churners
    senior_citizens = churners['SeniorCitizen'].value_counts()
    with col1:
        st.markdown(create_enhanced_stat_box(
            "Senior Citizen Churners",
            "👴",
            f"{senior_citizens.get('Yes', 0)}",
            f"{senior_citizens.get('Yes', 0) / len(churners):.1%} of churners"
        ), unsafe_allow_html=True)
        st.plotly_chart(create_small_donut_chart(churners, senior_citizens.values, senior_citizens.index, "Senior Citizen Churners"), use_container_width=True)

    # Churners with Partners
    partner_counts = churners['Partner'].value_counts()
    with col2:
        st.markdown(create_enhanced_stat_box(
            "Churners with Partners",
            "👫",
            f"{partner_counts.get('Yes', 0)}",
            f"{partner_counts.get('Yes', 0) / len(churners):.1%} of churners"
        ), unsafe_allow_html=True)
        st.plotly_chart(create_small_donut_chart(churners, partner_counts.values, partner_counts.index, "Churners with Partners"), use_container_width=True)

    # Churners with Phone Service
    phone_service_counts = churners['PhoneService'].value_counts()
    with col1:
        st.markdown(create_enhanced_stat_box(
            "Churners with Phone Service",
            "📞",
            f"{phone_service_counts.get('Yes', 0)}",
            f"{phone_service_counts.get('Yes', 0) / len(churners):.1%} of churners"
        ), unsafe_allow_html=True)
        st.plotly_chart(create_small_donut_chart(churners, phone_service_counts.values, phone_service_counts.index, "Churners with Phone Service"), use_container_width=True)

    # Payment Methods of Churners
    payment_methods_churners = churners['PaymentMethod'].value_counts()
    with col2:
        st.markdown(create_enhanced_stat_box(
            "Payment Methods of Churners",
            "💳",
            f"{len(payment_methods_churners)} types",
            f"Most common: {payment_methods_churners.index[0]}"
        ), unsafe_allow_html=True)
        st.plotly_chart(create_small_donut_chart(churners, payment_methods_churners.values, payment_methods_churners.index, "Payment Methods of Churners"), use_container_width=True)


# if __name__ == "__main__":
#     show_r_dash()