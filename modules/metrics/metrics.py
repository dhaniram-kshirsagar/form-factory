import streamlit as st
import pandas as pd
import math
from pathlib import Path

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
        ['Factory 3', 'Factory 5', 'Factory 7', 'Factory 10'])
    
    return selected_factories

def lineGraph(factory_profit_df, selected_factories, from_year, to_year):
        
    # Filter the data
    filtered_factory_df = factory_profit_df[
        (factory_profit_df['factory'].isin(selected_factories))
        & (factory_profit_df['Year'] <= to_year)
        & (from_year <= factory_profit_df['Year'])
    ]

    # filtered_factory_df['time'] = pd.to_datetime(filtered_factory_df['date'])
    # monthly_avg_df = (filtered_factory_df.groupby(['factory', 'time', filtered_factory_df['time'].dt.to_period('m')])['defect_rate_pcnt']
    #       .sum()
    #       .groupby(level=0)
    #       .mean()
    #       .reset_index(name='avg_defect_rate'))

    filtered_factory_df['time'] = pd.to_datetime(filtered_factory_df['date'])
    filtered_factory_df['MonthYear'] = filtered_factory_df['time'].apply("{:%Y-%m}".format)
    monthly_avg_df = filtered_factory_df.groupby([filtered_factory_df['MonthYear'], filtered_factory_df['factory']])['defect_rate_pcnt'].mean().reset_index()

    colgraph = st.columns(2)

    with colgraph[0]:
        st.header('Defect Rate', divider='gray')

        ''

        st.line_chart(
            monthly_avg_df,
            x='MonthYear',
            y='defect_rate_pcnt',
            color='factory',
        )

        ''
        ''

    avg_month_prod = filtered_factory_df.groupby([filtered_factory_df['MonthYear'], filtered_factory_df['factory']])['production_volume_units'].mean().reset_index()
    with colgraph[1]:
        st.header('Production Volume', divider='gray')

        ''

        st.line_chart(
            avg_month_prod,
            x='MonthYear',
            y='production_volume_units',
            color='factory',
        )
    
    ''
    ''

    colgraph2 = st.columns(2)

    avg_month_energy = filtered_factory_df.groupby([filtered_factory_df['MonthYear'], filtered_factory_df['factory']])['energy_consumption_kwh'].mean().reset_index()
    avg_month_dntime = filtered_factory_df.groupby([filtered_factory_df['MonthYear'], filtered_factory_df['factory']])['machine_downtime_hours'].mean().reset_index()

    with colgraph2[0]:
        st.header('Energy Consumption', divider='gray')

        ''

        st.line_chart(
            avg_month_energy,
            x='MonthYear',
            y='energy_consumption_kwh',
            color='factory',
        )

        ''
        ''

    with colgraph2[1]:
        st.header('Factory Uptime', divider='gray')

        ''

        st.line_chart(
            avg_month_dntime,
            x='MonthYear',
            y='machine_downtime_hours',
            color='factory',
        )


def metricsPage(factory_profit_df):
    from_year, to_year = yearFilter(factory_profit_df)
    selected_factories = selectedFactories(factory_profit_df)
    lineGraph(factory_profit_df, selected_factories, from_year, to_year)

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

 