from pathlib import Path
from modules.metrics import metrics as m
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)

def show_page():
    # creating a single-element container.
    placeholder = st.empty()

    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        churn_data = pd.read_csv(Path(__file__).parent.parent/'modules/data/telchurn/TelecomChurn.csv')
        # Calculate KPIs
        # 1. Churn Rate
        total_customers = len(churn_data)
        churned_customers = churn_data[churn_data['Churn'] == 'Yes']
        churn_rate = len(churned_customers) / total_customers * 100
        kpi1.metric(label="Churn Rate %", value=churn_rate)
        # 2. Average Tenure
        average_tenure = churn_data['tenure'].mean()
        kpi2.metric(label="Avg. Tenure (months)", value=average_tenure)
        # 3. Average Monthly Charges
        average_monthly_charges = churn_data['MonthlyCharges'].mean()
        kpi3.metric(label="Avg. Monthly Charges", value=round(average_monthly_charges,2))
        # 6. Percentage of Customers with Additional Services
        services = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
        percentage_additional_services = {}
        for service in services:
            percentage_additional_services[service] = (churn_data[service].value_counts(normalize=True).loc['Yes'])
            # Display results
            print(f"Churn Rate: {churn_rate:.2f}%")
            print(f"Average Tenure: {average_tenure:.2f} months")
            print(f"Average Monthly Charges: ${average_monthly_charges:.2f}")
            print("Percentage of Customers with Additional Services:")

        for service, percentage in percentage_additional_services.items():
            print(f"{service}: {percentage:.2f}%")    