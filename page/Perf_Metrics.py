from modules.metrics import metrics as m
import streamlit as st

def show_page():
    m.metricsPage()
    # with st.sidebar:
    #     st.write("Sidebar")