import streamlit as st
import pandas as pd
from io import StringIO
import joblib
from pathlib import Path
import plotly.express as px
import matplotlib.pyplot as plt
from utils.data_processing import clean_and_encode_data, clean_and_encode_data_for_7, encode_data
from utils.rag import create_rag_layer
from page.churn_bot import chatbot_prediction, chatbot_interface
from streamlit_option_menu import option_menu  # Import streamlit_option_menu

# Load the model
CHURN_REG_MODEL_FILE = Path(__file__).parent.parent / "modules/data/telchurn/gradient_boosting_model_new.joblib"
model = joblib.load(CHURN_REG_MODEL_FILE)

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
    print('Starting make_predictions')
    print('Input data shape:', input_data.to_csv(index=False))
    """Common prediction logic for both form and CSV inputs"""
    if input_data.shape[1] == 7:
        processed_df = clean_and_encode_data_for_7(input_data)
    else:
        processed_df = clean_and_encode_data(input_data)
    print('Processed DataFrame shape:', processed_df.to_csv(index=False))
    clean_columns = ['tenure', 'OnlineSecurity', 'OnlineBackup', 'TechSupport', 'Contract', 'MonthlyCharges', 'TotalCharges']
    processed_df = processed_df[clean_columns]
    print('Reduced final DataFrame shape:', processed_df.to_csv(index=False))
    predictions = model.predict(processed_df)
    print('Predictions:', predictions[:5])
    proba = model.predict_proba(processed_df)[:, 1] if hasattr(model, 'predict_proba') else None
    print('Probabilities:', proba[:5] if proba is not None else 'No probabilities')

    result_df = input_data.copy()
    result_df['Prediction'] = ['Churn' if p == 1 else 'No Churn' for p in predictions]
    if proba is not None:
        result_df['Churn Probability'] = proba

    print('Completed make_predictions')
    return result_df, proba

def show_predictions(result_df, proba):
    print('Starting show_predictions')
    print('Result DataFrame shape:', result_df.shape)
    """Display prediction results and visualizations"""
    st.subheader("Prediction Results")

    if proba is not None:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(result_df, names='Prediction',
                        title='Churn vs No Churn Distribution')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.histogram(result_df, x='Churn Probability', nbins=20,
                              title='Distribution of Churn Probabilities')
            st.plotly_chart(fig, use_container_width=True)

    st.dataframe(result_df, use_container_width=True)
    print('Completed show_predictions')

def show_form_input():
    st.header("Predict Churn with Form Input")
    with st.form("customer_form"):
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, step=1)
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
        online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0)
        total_charges = st.number_input("Total Charges ($)", min_value=0.0)

        submitted = st.form_submit_button("Predict Churn")
        if submitted:
            customer = {
                "tenure": tenure,
                "Contract": contract,
                "OnlineSecurity": online_security,
                "OnlineBackup": online_backup,
                "TechSupport": tech_support,
                "MonthlyCharges": monthly_charges,
                "TotalCharges": total_charges,
            }

            input_df = pd.DataFrame([customer])
            result_df, proba = make_predictions(model, input_df)
            show_predictions(result_df, proba)

def show_csv_upload():
    st.header("Predict Churn with CSV Upload")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            required_columns = set([
                'tenure', 'Contract', 'OnlineSecurity', 'OnlineBackup', 'TechSupport',
                'MonthlyCharges', 'TotalCharges',
            ])
            if required_columns.issubset(df.columns):
                if st.button("Predict Churn"):
                    result_df, proba = make_predictions(model, df)
                    show_predictions(result_df, proba)
            else:
                st.error("CSV file missing required columns")
        except Exception as e:
            print(e)
            st.error(f"Error processing CSV file: {str(e)}")

def show_churn_pred():
    set_custom_css()
    st.title("Customer Churn Astro - Predicts Churn!")

    # Create two columns for the layout
    col1, col2 = st.columns([1.5, 2.5])

    # Menu in the first column
    with col1:
        st.subheader("Menu")
        selected_option = option_menu(
            "Select Input for Prediction",
            ["Form Input", "CSV Upload"],
            icons=['file-earmark-person', 'upload'],
            menu_icon="cast", default_index=0,
        )

        st.markdown("---")
        st.subheader("Astro Bot! Looking for churn predictions?")
        st.text('We uses defaults for missing values!')
        chatbot_interface(model)

    # Content in the second column
    with col2:
        if selected_option == "Form Input":
            show_form_input()
        elif selected_option == "CSV Upload":
            show_csv_upload()

# if __name__ == "__main__":
#     main()