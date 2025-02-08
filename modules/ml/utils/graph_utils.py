"""
Graph Utilities Module

This module contains functions for generating and displaying various graphs
in the telecom churn prediction page.
"""

import streamlit as st
import plotly.express as px
import pandas as pd


def lineGraph_rev(factory_profit_df, selected_factories, selected_locations, from_month, to_month):
    """
    Generate and display revenue line graph

    Args:
        factory_profit_df: DataFrame containing the revenue data
        selected_factories: List of selected factories to display
        selected_locations: List of selected locations to display
        from_month: Start month for the graph
        to_month: End month for the graph
    """
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
                bonus_index = sorted(selected_locations).index(location)
                return revenue + (bonus_index + 1) * 100000
            return revenue

        filtered_factory_df['Adjusted Revenue'] = filtered_factory_df.apply(adjust_revenue, axis=1)

        st.header('Predicted Revenue ($) for Six Months', divider='gray')

        fig = px.line(
            filtered_factory_df, 
            x='Month', 
            y='Adjusted Revenue', 
            color='Location', 
        )
        fig.update_layout(
            yaxis_title="Adjusted Revenue ($)<br><sup>(Divide the given value by 100000 to see the exact prediction)</sup>" 
        )
        st.plotly_chart(fig)


def lineGraph_foam(factory_profit_df, selected_factories, selected_locations, from_month, to_month):
    """
    Generate and display foam density line graph

    Args:
        factory_profit_df: DataFrame containing the foam density data
        selected_factories: List of selected factories to display
        selected_locations: List of selected locations to display
        from_month: Start month for the graph
        to_month: End month for the graph
    """
    filtered_factory_df = factory_profit_df[
        factory_profit_df['Factory'].isin(selected_factories)
        & factory_profit_df['Location'].isin(selected_locations)
        & (factory_profit_df['Month'] <= to_month)
        & (from_month <= factory_profit_df['Month'])
    ].copy()

    if not filtered_factory_df.empty:
        def adjust_foam(row):
            location = row['Location']
            Predicted_Foam_Density = row['Predicted Foam Density']
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
    """
    Generate and display production volume line graph

    Args:
        factory_profit_df: DataFrame containing the production volume data
        selected_factories: List of selected factories to display
        selected_locations: List of selected locations to display
        from_month: Start month for the graph
        to_month: End month for the graph
    """
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
