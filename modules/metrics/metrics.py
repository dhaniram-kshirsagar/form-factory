import streamlit as st
import pandas as pd
import math
from pathlib import Path

def selectedFactories(factory_profit_df):
    factories = factory_profit_df['FactoryID'].unique()

    selected_factories = st.multiselect(
        'Which factories would you like to view?',
        factories,
        ['F1', 'F2', 'F3', 'F4', 'F5', 'F6'])
    
    return selected_factories

def lineGraph(factory_profit_df, selected_factories):
        
    # Filter the data
    filtered_factory_df = factory_profit_df[
        (factory_profit_df['FactoryID'].isin(selected_factories))
    ]

    colgraph = st.columns(2)

    with colgraph[0]:
        st.header('Factory Profit Graph over time', divider='gray')

        ''

        st.line_chart(
            filtered_factory_df,
            x='Date',
            y='TotalProfit',
            color='FactoryID',
        )

        ''
        ''

    with colgraph[1]:
        st.header('Factorywise Profit Per Unit Graph over time', divider='gray')

        ''

        st.line_chart(
            filtered_factory_df,
            x='Date',
            y='ProfitPerUnit',
            color='FactoryID',
        )

def metricsPage(factory_profit_df):
    selected_factories = selectedFactories(factory_profit_df)
    lineGraph(factory_profit_df, selected_factories)

    ''
    ''

""" 
    cols = st.columns(4)

    for i, country in enumerate(selected_countries):
        col = cols[i % len(cols)]

        with col:
            first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
            last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000

            if math.isnan(first_gdp):
                growth = 'n/a'
                delta_color = 'off'
            else:
                growth = f'{last_gdp / first_gdp:,.2f}x'
                delta_color = 'normal'

            st.metric(
                label=f'{country} GDP',
                value=f'{last_gdp:,.0f}B',
                delta=growth,
                delta_color=delta_color
            ) """

 