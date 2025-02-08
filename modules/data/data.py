import streamlit as st
import pandas as pd
import math
from pathlib import Path

@st.cache_data
def getFactoryDataProfit(): 
    DATA_FILENAME = Path(__file__).parent.parent/'data/large-data/FoamFactory_V2_27K.csv'
    raw_profit_df =  pd.read_csv(DATA_FILENAME)
    selected_columns = ['Factory', 'Date', 'Production Volume (units)', 'Cost of Downtime ($)', 'Profit Margin (%)'] 
    # Create a new DataFrame with the selected columns
    df_selected = raw_profit_df[selected_columns]
    return raw_profit_df

@st.cache_data
def getFactoryComplexDataProfit(): 
    DATA_FILENAME = Path(__file__).parent.parent/'data/large-data/FoamFactory_V2_27K.csv'
    raw_df =  pd.read_csv(DATA_FILENAME)

    from os import replace

    col_rename_lst = {}
    for series_name, series in raw_df.items():
        col_rename_lst[series_name] = series_name.replace(' ','_').replace('%','pcnt').replace('(','').replace(')','').replace('$','dolrs').lower()
    raw_df = raw_df.rename(columns=col_rename_lst)

    return raw_df