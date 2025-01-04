import streamlit as st
import pandas as pd
import math
from pathlib import Path
import plotly.express as px

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
        [0])  # add sample factory

    return selected_factories


def selectedLocations(factory_profit_df):
    locations = factory_profit_df['Location'].unique()
    selected_locations = st.multiselect(
        'Which location would you like to view?',
        locations,
        locations[:4] if len(locations) >= 4 else locations
    )
    return selected_locations

def lineGraph_rev(factory_profit_df, selected_factories, selected_locations, from_month, to_month):
    # Filter the data
    filtered_factory_df = factory_profit_df[
        factory_profit_df['Factory'].isin(selected_factories)
        & factory_profit_df['Location'].isin(selected_locations)
        & (factory_profit_df['Month'] <= to_month)
        & (from_month <= factory_profit_df['Month'])
    ].copy()

    if not filtered_factory_df.empty:
        def adjust_revenue(row):
            location = row['Location']
            revenue = row['Predicted Revenue ($)']
            if location in selected_locations:
                bonus_index = sorted(selected_locations).index(location) #index of the sorted locations
                return revenue + (bonus_index + 1) * 100000
            return revenue

        filtered_factory_df['Adjusted Revenue'] = filtered_factory_df.apply(adjust_revenue, axis=1)

        st.header('Predicted Revenue ($) for Six Months', divider='gray')

        fig = px.line(
            filtered_factory_df, 
            x='Month', 
            y='Adjusted Revenue', 
            color='Location', 
          #  title='Predicted Revenue ($) for Six Months'
        )
        # fig.add_annotation(
        #     text="This is a custom footer for Revenue Graph.", 
        #     xref="paper", yref="paper", 
        #     x=1, y=0, 
        #     showarrow=False, 
        #     font=dict(size=10)
        # )
        fig.update_layout(
            yaxis_title="Adjusted Revenue ($)<br><sup>(Divide the given value by 100000 to see the exact prediction)</sup>" 
        )

        st.plotly_chart(fig)

       # st.markdown(f"<p style='text-align: center;'>'helllo'</p>", unsafe_allow_html=True)

def lineGraph_foam(factory_profit_df, selected_factories, selected_locations, from_month, to_month):
    filtered_factory_df = factory_profit_df[
        factory_profit_df['Factory'].isin(selected_factories)
        & factory_profit_df['Location'].isin(selected_locations)
        & (factory_profit_df['Month'] <= to_month)
        & (from_month <= factory_profit_df['Month'])
    ].copy()

    if not filtered_factory_df.empty:
        def adjust_foam(row): #same logic for foam
            location = row['Location']
            Predicted_Foam_Density = row['Predicted Foam Density']  # assuming you have a 'Foam' column
            if location in selected_locations:
                bonus_index = sorted(selected_locations).index(location)
                return Predicted_Foam_Density + (bonus_index + 1) * 120000
            return Predicted_Foam_Density

        filtered_factory_df['Predicted Foam Density'] = filtered_factory_df.apply(adjust_foam, axis=1)

    st.header('Predicted Foam Density for Six Months', divider='gray')

    fig = px.line(
        filtered_factory_df, 
        x='Month', 
        y='Predicted Foam Density', 
        color='Location', 
        title='Predicted Foam Density for Six Months'
    )
    fig.update_layout(
            yaxis_title="Predicted Foam Density <br><sup>(Divide the given value by 120000 to see the exact prediction)</sup>" 
        )
    st.plotly_chart(fig)

def lineGraph_vol(factory_profit_df, selected_factories, selected_locations, from_month, to_month):

    # Filter the data
    filtered_factory_df = factory_profit_df[
        factory_profit_df['Factory'].isin(selected_factories)
        & factory_profit_df['Location'].isin(selected_locations)
        & (factory_profit_df['Month'] <= to_month)
        & (from_month <= factory_profit_df['Month'])
    ]
    if not filtered_factory_df.empty:
        def adjust_volume(row):
            location = row['Location']
            volume = row['Predicted Production Volume (units)']
            if location in selected_locations:
                bonus_index = sorted(selected_locations).index(location)
                return volume + (bonus_index + 1) * 100000
            return volume

        filtered_factory_df['Predicted Production Volume (units)'] = filtered_factory_df.apply(adjust_volume, axis=1)

    st.header('Predicted Production Volume (units) for Six Months', divider='gray')

    fig = px.line(
        filtered_factory_df, 
        x='Month', 
        y='Predicted Production Volume (units)', 
        color='Location', 
        title='Predicted Production Volume (units) for Six Months'
    )
    fig.update_layout(
            yaxis_title="Predicted Production Volume (units) <br><sup>(Reduce the given value by 100000 to see the exact prediction)</sup>" 
        )
    st.plotly_chart(fig)

def predictionPage(result_vol_df,result_rev_df,result_foam_df):
    from_year, to_year = yearFilter(result_vol_df)
    selected_factories = selectedFactories(result_vol_df)
    selected_locations = selectedLocations(result_vol_df)
    lineGraph_vol(result_vol_df, selected_factories, selected_locations, from_year, to_year)
    lineGraph_rev(result_rev_df, selected_factories, selected_locations, from_year, to_year)
    lineGraph_foam(result_foam_df, selected_factories, selected_locations, from_year, to_year)