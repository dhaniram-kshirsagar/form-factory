import streamlit as st
import pandas as pd
import math
from pathlib import Path
from modules.data.data_curater import load_data

def yearFilter(factory_profit_df): 

    min_value = factory_profit_df['Year'].min()
    max_value = factory_profit_df['Year'].max()

    from_year, to_year = st.slider(
        'Which years are you interested in?',
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value])

    return from_year, to_year

def selectedFactories(factory_profit_df):
    factories = factory_profit_df['factory'].unique()

    selected_factories = st.multiselect(
        'Which factories would you like to view?',
        factories,
        ['Factory 3', 'Factory 5'])
    
    return selected_factories

def defect_rate(factory_profit_df, selected_factories, from_year, to_year):
        
    # Filter the data
    filtered_factory_df = factory_profit_df[
        (factory_profit_df['factory'].isin(selected_factories))
        & (factory_profit_df['Year'] <= to_year)
        & (from_year <= factory_profit_df['Year'])
    ]
    
    st.header('Defect Rate', divider='gray')

    ''

    st.line_chart(
        filtered_factory_df,
        x='MonthYear',
        y='defect_rate_pcnt',
        color='factory',
    )

    ''
    ''

def lineGraph2(factory_profit_df, selected_factories, from_year, to_year):

    
    filtered_factory_df = factory_profit_df[
        (factory_profit_df['factory'].isin(selected_factories))
        & (factory_profit_df['Year'] <= to_year)
        & (from_year <= factory_profit_df['Year'])
    ]
    
    st.header('Production Volume', divider='gray')

    ''

    st.line_chart(
        filtered_factory_df,
        x='MonthYear',
        y='production_volume_units',
        color='factory',
    )

    ''
    ''

def lineGraph3( factory_profit_df,selected_factories, from_year, to_year):

    filtered_factory_df = factory_profit_df[
        (factory_profit_df['factory'].isin(selected_factories))
        & (factory_profit_df['Year'] <= to_year)
        & (from_year <= factory_profit_df['Year'])
    ]
    
    st.header('Energy Consumption', divider='gray')

    ''

    st.line_chart(
        filtered_factory_df,
        x='MonthYear',
        y='energy_consumption_kwh',
        color='factory',
    )

    ''
    ''


def lineGraph4(factory_profit_df, selected_factories, from_year, to_year):
    filtered_factory_df = factory_profit_df[
        (factory_profit_df['factory'].isin(selected_factories))
        & (factory_profit_df['Year'] <= to_year)
        & (from_year <= factory_profit_df['Year'])
    ]
    
    st.header('Factory Uptime', divider='gray')

    ''

    st.line_chart(
        filtered_factory_df,
        x='MonthYear',
        y='machine_downtime_hours',
        color='factory',
    )


def metricsPage():
    avg_defect_rate_df=load_data('avg_defect_rate_table')
    from_year, to_year = yearFilter(avg_defect_rate_df)
    selected_factories = selectedFactories(avg_defect_rate_df)

    colgraph = st.columns(2)

    with colgraph[0]:
        
        defect_rate(avg_defect_rate_df, selected_factories, from_year, to_year)
    with colgraph[1]:
        production_volume_units = load_data('production_volume_units')

        lineGraph2( production_volume_units,selected_factories, from_year, to_year)

    colgraph2 = st.columns(2)
    
    with colgraph2[0]:
        energy_consumption_kwh = load_data('energy_consumption_kwh')
        lineGraph3(energy_consumption_kwh,selected_factories, from_year, to_year)
    with colgraph2[1]:
        machine_downtime_hours = load_data('machine_downtime_hours')
        lineGraph4( machine_downtime_hours,selected_factories, from_year, to_year)

    ''
    ''


 