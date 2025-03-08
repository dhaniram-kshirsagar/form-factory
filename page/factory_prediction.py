import streamlit as st
import pandas as pd
from io import StringIO
import joblib
from pathlib import Path
import plotly.express as px
import matplotlib.pyplot as plt
from utils.data_processing import clean_and_encode_revenue_data
from utils.rag import create_rag_layer
from page.factory_pred_bot import chatbot_prediction, chatbot_interface
from streamlit_option_menu import option_menu

# Feature keys and mean values
keys_revenue = [
    "month", "year", "Factory", "Location", "Cycle Time (minutes)", 
    "Product Category", "Waste Generated (kg)", "Production Volume (units)",
    "Water Usage (liters)", "Machine Utilization (%)",
    "Machine Age (years)", "Machine Type", "Supplier", "Operator Experience (years)"
]

values_row_2 = [
    0, 6.521072796934866, 2022.0, 2.0, 2.0, 20.02371829958037, 
    1.0023718299580369, 297.2048896186827, 680.4226195949644, 
    6269.731800766283, 73.59872286079182, 6.0622437511403025, 
    1.0023718299580369, 1.0694033935413245, 4.963446086480569
]

# Load the revenue model
REVENUE_MODEL_FILE = Path(__file__).parent.parent / "modules/ml/revenue_prediction_model.pkl"
model = joblib.load(REVENUE_MODEL_FILE)

# Custom CSS for professional theming
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
        color: #003366;
        border: 1px solid rgba(var(--primary-color-rgb), 0.2);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
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
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
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
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
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

def make_predictions(model, input_data):
    # Fill missing values with mean values
    for i, key in enumerate(keys_revenue):
        if key not in input_data.columns:
            input_data[key] = values_row_2[i]
    
    processed_df = clean_and_encode_revenue_data(input_data)
    predictions = model.predict(processed_df)
    proba = model.predict_proba(processed_df)[:, 1] if hasattr(model, 'predict_proba') else None
    return predictions, proba

def show_predictions(result_df, proba):
    st.subheader("Prediction Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Predicted Revenue", f"${result_df['Predicted Revenue ($)'].iloc[0]:,.2f}")
    with col2:
        if proba is not None:
            st.metric("Confidence", f"{proba[0]*100:.1f}%")
    
    fig = px.bar(result_df, x='Factory', y='Predicted Revenue ($)', 
                 color='Product Category', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

def show_form_input():
    with st.form("revenue_prediction_form"):
        st.subheader("Factory Revenue Prediction Form")
        
        col1, col2 = st.columns(2)
        with col1:
            month = st.number_input("Month", min_value=1, max_value=12, value=int(values_row_2[0]))
            year = st.number_input("Year", min_value=2020, max_value=2030, value=int(values_row_2[1]))
            factory = st.selectbox("Factory", options=[f"Factory {i+1}" for i in range(10)], index=int(values_row_2[2]))
            location = st.selectbox("Location", options=["City A", "City B", "City C", "City D", "City E"], index=int(values_row_2[3]))
            cycle_time = st.number_input("Cycle Time (minutes)", value=values_row_2[4])
            product_category = st.selectbox("Product Category", options=["A", "B", "C"], index=int(values_row_2[5]))
        with col2:
            waste_generated = st.number_input("Waste Generated (kg)", value=values_row_2[6])
            production_volume = st.number_input("Production Volume (units)", value=values_row_2[7])
            water_usage = st.number_input("Water Usage (liters)", value=values_row_2[8])
            machine_utilization = st.slider("Machine Utilization (%)", 0, 100, value=int(values_row_2[9]))
            machine_age = st.number_input("Machine Age (years)", value=values_row_2[10])
            machine_type = st.selectbox("Machine Type", options=["Type A", "Type B", "Type C"], index=int(values_row_2[11]))
            supplier = st.selectbox("Supplier", options=["Supplier A", "Supplier B", "Supplier C"], index=int(values_row_2[12]))
            operator_experience = st.number_input("Operator Experience (years)", value=values_row_2[13])
        
        submitted = st.form_submit_button("Predict Revenue")
        if submitted:
            input_data = pd.DataFrame([{
                'month': month,
                'year': year,
                'Factory': factory,
                'Location': location,
                'Cycle Time (minutes)': cycle_time,
                'Product Category': product_category,
                'Waste Generated (kg)': waste_generated,
                'Production Volume (units)': production_volume,
                'Water Usage (liters)': water_usage,
                'Machine Utilization (%)': machine_utilization,
                'Machine Age (years)': machine_age,
                'Machine Type': machine_type,
                'Supplier': supplier,
                'Operator Experience (years)': operator_experience
            }])
            predictions, proba = make_predictions(model, input_data)
            result_df = input_data.copy()
            result_df['Predicted Revenue ($)'] = predictions
            show_predictions(result_df, proba)

def show_csv_upload():
    st.subheader("Batch Revenue Prediction")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(input_df.head())
        
        if st.button("Run Batch Prediction"):
            predictions, proba = make_predictions(model, input_df)
            result_df = input_df.copy()
            result_df['Predicted Revenue ($)'] = predictions
            show_predictions(result_df, proba)

def show_pred():
    set_custom_css()
    st.title('Factory Revenue Prediction')
    
    selected = option_menu(
        menu_title=None,
        options=['Form Input', 'CSV Upload', 'Chatbot'],
        icons=['input-cursor-text', 'file-earmark-arrow-up', 'robot'],
        menu_icon='cast',
        default_index=0,
        orientation='horizontal'
    )
    
    if selected == 'Form Input':
        show_form_input()
    elif selected == 'CSV Upload':
        show_csv_upload()
    elif selected == 'Chatbot':
        chatbot_interface(model)
