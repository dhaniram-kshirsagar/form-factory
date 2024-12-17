import streamlit as st

from modules.data import data

from modules.performance import performance as p

st.set_page_config(
    page_title="Foam Factory Performance",
    page_icon="🤖"
)

st.header('🤖  Foam Factory Performance')

gdp_df = data.get_gdp_data()
p.performancePage(gdp_df)