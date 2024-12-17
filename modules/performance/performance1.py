import streamlit as st
import pandas as pd
import math
from pathlib import Path


def yearFilter(gdp_df): 

    min_value = gdp_df['Year'].min()
    max_value = gdp_df['Year'].max()

    from_year, to_year = st.slider(
        'Which years are you interested in?',
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value])

    return from_year, to_year
    
    
def selectedCountry(gdp_df) :
    countries = gdp_df['Country Code'].unique()

    if not len(countries):
        st.warning("Select at least one country")

    selected_countries = st.multiselect(
        'Which countries would you like to view?',
        countries,
        ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'])
    
    return selected_countries

def lineGraph(gdp_df, selected_countries, from_year, to_year):
        
    # Filter the data
    filtered_gdp_df = gdp_df[
        (gdp_df['Country Code'].isin(selected_countries))
        & (gdp_df['Year'] <= to_year)
        & (from_year <= gdp_df['Year'])
    ]

    colgraph = st.columns(2)

    with colgraph[0]:
        st.header('GDP123', divider='gray')

        ''

        st.line_chart(
            filtered_gdp_df,
            x='Year',
            y='GDP',
            color='Country Code',
        )

        ''
        ''

    with colgraph[1]:
        st.header('GDP over time', divider='gray')

        ''

        st.line_chart(
            filtered_gdp_df,
            x='Year',
            y='GDP',
            color='Country Code',
        )

def performancePage(gdp_df):
    from_year, to_year = yearFilter(gdp_df)
    selected_countries = selectedCountry(gdp_df)

    lineGraph(gdp_df, selected_countries, from_year, to_year)

    ''
    ''

    first_year = gdp_df[gdp_df['Year'] == from_year]
    last_year = gdp_df[gdp_df['Year'] == to_year]

    st.header(f'GDP in {to_year}', divider='gray')

    ''

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
            )



