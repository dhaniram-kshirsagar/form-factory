"""
Filter Utilities Module

This module contains functions for filtering and selecting data in the telecom churn prediction system.
"""

import streamlit as st
import pandas as pd


def yearFilter(factory_profit_df):
    """
    Create a year filter widget

    Args:
        factory_profit_df: DataFrame containing the data to filter

    Returns:
        Tuple of (from_year, to_year) selected in the filter
    """
    min_value = factory_profit_df['Month'].min()
    max_value = factory_profit_df['Month'].max()

    from_year, to_year = st.slider(
        'Which months are you interested in?',
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value])

    return from_year, to_year


def selectedFactories(factory_profit_df):
    """
    Create a factory selection widget

    Args:
        factory_profit_df: DataFrame containing the factory data

    Returns:
        List of selected factories
    """
    factories = factory_profit_df['Factory'].unique()

    selected_factories = st.multiselect(
        'Which factories would you like to view?',
        factories,
        [0])

    return selected_factories


def selectedLocations(factory_profit_df):
    """
    Create a location selection widget

    Args:
        factory_profit_df: DataFrame containing the location data

    Returns:
        List of selected locations
    """
    locations = factory_profit_df['Location'].unique()
    selected_locations = st.multiselect(
        'Which location would you like to view?',
        locations,
        locations[:4] if len(locations) >= 4 else locations
    )
    return selected_locations
