import streamlit as st
import pandas as pd
import math
from pathlib import Path

@st.cache_data
def get_gdp_data():
    """Grab Foam factory data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent.parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and GDP
    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df


@st.cache_data
def getFactoryDataProfit(): 
    DATA_FILENAME = Path(__file__).parent.parent/'data/sample-data/factorydata.csv'
    raw_profit_df =  pd.read_csv(DATA_FILENAME)
    selected_columns = ['FactoryID', 'Date', 'ProductionVolume', 'TotalProfit', 'ProfitPerUnit'] 
    # Create a new DataFrame with the selected columns
    df_selected = raw_profit_df[selected_columns]
    return raw_profit_df

@st.cache_data
def getFactoryComplexDataProfit(): 
    DATA_FILENAME = Path(__file__).parent.parent/'data/large-data/Complex_Expanded_Factory_Data.csv'
    raw_df =  pd.read_csv(DATA_FILENAME)

    from os import replace

    col_rename_lst = {}
    for series_name, series in raw_df.items():
        col_rename_lst[series_name] = series_name.replace(' ','_').replace('%','pcnt').replace('(','').replace(')','').replace('$','dolrs').lower()
    raw_df = raw_df.rename(columns=col_rename_lst)

    return raw_df

from llama_index.core import SimpleDirectoryReader

@st.cache_resource(show_spinner=False)
def load_data_for_llm():
    reader = SimpleDirectoryReader(input_dir=Path(__file__).parent.parent/'data/large-data', recursive=True)
    return reader.load_data()