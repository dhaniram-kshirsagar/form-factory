import streamlit as st
import pandas as pd
from modules.data import data

from modules.performance import performance as p
def show_currentPerformance():
    # st.set_page_config(
    #     page_title="Performance",
    #     page_icon="🤖",
    #     layout='wide',
    # )

    st.subheader('🤖  Current Performance')

    factories_df = data.getFactoryDataProfit()
    factories_df['Year'] = pd.DatetimeIndex(factories_df['Date']).year
    factories_df['Month'] = pd.DatetimeIndex(factories_df['Date']).month

    p.performancePage(factories_df)