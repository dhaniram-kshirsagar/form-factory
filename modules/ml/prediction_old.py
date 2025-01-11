import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt

def yearFilter(factory_profit_df): 

    min_value = factory_profit_df['Month'].min()
    max_value = factory_profit_df['Month'].max()

    from_year, to_year = st.slider(
        'Which months are you interested in?',
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value])

    return from_year, to_year

def selectedFactories(factory_profit_df):
    factories = factory_profit_df['Factory'].unique()

    selected_factories = st.multiselect(
        'Which factories would you like to view?',
        factories,
        [0])                                             #add sample factory
    
    return selected_factories

def selectedLocations(factory_profit_df):
    factories = factory_profit_df['Location'].unique()

    selected_factories = st.multiselect(
        'Which location would you like to view?',
        factories,
        [0, 1, 2, 3])                                             #add sample factory
    
    return selected_factories

def lineGraph_rev(factory_profit_df, selected_factories, selected_locations, from_month, to_month):
        
    # Filter the data
    filtered_factory_df = factory_profit_df[
        factory_profit_df['Factory'].isin(selected_factories)
        & factory_profit_df['Location'].isin(selected_locations)
        & (factory_profit_df['Month'] <= to_month)
        & (from_month <= factory_profit_df['Month'])
    ]


    st.header('Predicted Revenue ($) for Six Months', divider='gray')

    ''

    st.bar_chart(
        filtered_factory_df,
        x='Month',
        y='Predicted Revenue ($)',
        color='Location',
    )

    ''
    ''

def lineGraph_foam(factory_profit_df, selected_factories, selected_locations, from_month, to_month):
        
    # Filter the data
    filtered_factory_df = factory_profit_df[
        factory_profit_df['Factory'].isin(selected_factories)
        & factory_profit_df['Location'].isin(selected_locations)
        & (factory_profit_df['Month'] <= to_month)
        & (from_month <= factory_profit_df['Month'])
    ]


    filtered_factory_df['Predicted Foam Density'] = filtered_factory_df['Predicted Foam Density'] * 100000
    filtered_factory_df['Predicted Foam Density'] = filtered_factory_df['Predicted Foam Density'] - 120000


    st.header('Predicted Foam Density for Six Months', divider='gray')

    ''

    st.bar_chart(
        filtered_factory_df,
        x='Month',
        y='Predicted Foam Density',
        color='Location',
    )

    # chart_df = alt.Chart(filtered_factory_df).mark_line().encode(
    #     y=alt.Y('Predicted Foam Density', scale=alt.Scale(domain=[4680, 4690], clamp=True)),
    #     x=alt.X('Month'),
    #     color='Location'
    # )

    # st.altair_chart(chart_df)

    # fig = plt.figure(figsize=(12, 8))
    # ax = sns.lineplot(x='Month', y='Predicted Foam Density', hue='Location', 
    #          data=filtered_factory_df,
    #          palette=['red', 'blue', 'purple', 'pink'])
    # ax.set_ylim([1.241,1.250])

    # st.pyplot(fig)

    ''
    ''

def lineGraph_vol(factory_profit_df, selected_factories, selected_locations, from_month, to_month):
        
    # Filter the data
    filtered_factory_df = factory_profit_df[
        factory_profit_df['Factory'].isin(selected_factories)
        & factory_profit_df['Location'].isin(selected_locations)
        & (factory_profit_df['Month'] <= to_month)
        & (from_month <= factory_profit_df['Month'])
    ]


    st.header('Predicted Production Volume (units) for Six Months', divider='gray')

    ''

    st.bar_chart(
        filtered_factory_df,
        x='Month',
        y='Predicted Production Volume (units)',
        color='Location',
    )

    ''
    ''

def predictionPage(result_vol_df,result_rev_df,result_foam_df):
    from_year, to_year = yearFilter(result_vol_df)
    selected_factories = selectedFactories(result_vol_df)
    selected_locations = selectedLocations(result_vol_df)
    lineGraph_vol(result_vol_df, selected_factories, selected_locations, from_year, to_year)
    lineGraph_rev(result_rev_df, selected_factories, selected_locations, from_year, to_year)
    lineGraph_foam(result_foam_df, selected_factories, selected_locations, from_year, to_year)

    ''
    ''


 