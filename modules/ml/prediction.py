import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import math



def yearFilter(factory_profit_df): 
    min_value = factory_profit_df['Month'].min()
    max_value = factory_profit_df['Month'].max()

    from_year, to_year = st.slider(
        'Which months are you interested in?',
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value]
    )

    return from_year, to_year

def selectedFactories(factory_profit_df):
    factories = factory_profit_df['Factory'].unique()

    selected_factories = st.multiselect(
        'Which factories would you like to view?',
        factories,
        [factories[0]] if len(factories) > 0 else []
    )

    return selected_factories

def selectedLocations(factory_profit_df):
    locations = factory_profit_df['Location'].unique()

    selected_locations = st.multiselect(
        'Which location would you like to view?',
        locations,
        locations[:4] if len(locations) >= 4 else locations
    )

    return selected_locations

# Line graph for revenue
def lineGraph_rev(factory_profit_df, selected_factories, selected_locations, from_month, to_month, log_scale=False):
    # Filter the data
    filtered_factory_df = factory_profit_df[
        (factory_profit_df['Factory'].isin(selected_factories)) &
        (factory_profit_df['Location'].isin(selected_locations)) &
        (factory_profit_df['Month'] <= to_month) &
        (factory_profit_df['Month'] >= from_month)
    ]

    if filtered_factory_df.empty:
        st.warning("No data available for the selected filters (Factories, Locations, Months).")
        return
    
    # Check if the required column exists
    if 'Predicted Revenue ($)' not in filtered_factory_df.columns:
        st.error("The column 'Predicted Revenue ($)' is not present in the dataframe.")
        return

    # Apply transformations for hover data
    filtered_factory_df['Transformed Revenue'] = filtered_factory_df['Predicted Revenue ($)']
    filtered_factory_df['Transformed Revenue'] += np.random.uniform(-1000, 1000, size=len(filtered_factory_df))

    # Create a copy of the dataframe for hover data
    hover_df = filtered_factory_df[['Month', 'Location', 'Transformed Revenue']].copy()

    # Plot the graph
    st.header('Predicted Revenue ($)', divider='gray')

    fig = px.line(
        filtered_factory_df,
        x='Month',
        y='Predicted Revenue ($)',  # Use original values for the y-axis
        color='Location',
        hover_data=hover_df  # Use hover_df to avoid conflicts
    )

   
    st.plotly_chart(fig)

    # Add table with preview (5 rows) and expand for full table
    st.subheader("Predicted Data for Revenue")
    st.write("Preview of Predicted data (first 5 rows):")
    try:
        st.table(filtered_factory_df[['Month', 'Factory', 'Location', 'Predicted Revenue ($)']].head(5))
        with st.expander("Show Full Table"):
             st.write("Full Predicted data:")
             st.dataframe(filtered_factory_df)
    except KeyError as e:
        st.error(f"KeyError: {e}. Please ensure the required columns exist in the dataframe.")

# Line graph for foam density
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

   

    # Add table with preview (5 rows) and expand for full table
    st.subheader("Predicted Data for Foam Density")
    st.write("Preview of Predicted data (first 5 rows):")
    st.table(filtered_factory_df[['Month', 'Factory', 'Location', 'Predicted Foam Density']].head(5))

    with st.expander("Show Full Table"):
        st.write("Full Predicted data:")
        st.dataframe(filtered_factory_df)


# Line graph for production volume
def lineGraph_vol(factory_profit_df, selected_factories, selected_locations, from_month, to_month, log_scale=False):
    # Filter the data
    filtered_factory_df = factory_profit_df[
        (factory_profit_df['Factory'].isin(selected_factories)) &
        (factory_profit_df['Location'].isin(selected_locations)) &
        (factory_profit_df['Month'] <= to_month) &
        (factory_profit_df['Month'] >= from_month)
    ].copy()

    if filtered_factory_df.empty:
        st.warning("No data available for the selected filters (Factories, Locations, Months).")
        return

    y_axis_title = "Predicted Production Volume (units)"

    # Apply transformations for hover data
    filtered_factory_df['Transformed Volume'] = filtered_factory_df['Predicted Production Volume (units)']
    filtered_factory_df['Transformed Volume'] += np.random.uniform(-10, 10, size=len(filtered_factory_df))


    st.header('Predicted Production Volume', divider='gray')

    # Plot the graph
    fig = px.line(
        filtered_factory_df,
        x='Month',
        y='Predicted Production Volume (units)',
        color='Location',
        hover_data={
            'Log/Transformed Volume': filtered_factory_df['Transformed Volume']  # Avoid conflict
        }
    )

    
    st.plotly_chart(fig)


    # Add table with preview (5 rows) and expand for full table
    st.subheader("Predicted Data for Production Volume")
    st.write("Preview of Predicted data (first 5 rows):")
    st.table(filtered_factory_df[['Month', 'Factory', 'Location', 'Predicted Production Volume (units)']].head(5))

    with st.expander("Show Full Table"):
        st.write("Full Predicted data:")
        st.dataframe(filtered_factory_df)


# Prediction page combining all graphs
def predictionPage(result_vol_df, result_rev_df, result_foam_df):
    from_year, to_year = yearFilter(result_vol_df)
    selected_factories = selectedFactories(result_vol_df)
    selected_locations = selectedLocations(result_vol_df)

    #log_scale = st.checkbox("Use Logarithmic Scale for Y-Axis", value=False)

    lineGraph_vol(result_vol_df, selected_factories, selected_locations, from_year, to_year)
    lineGraph_rev(result_rev_df, selected_factories, selected_locations, from_year, to_year)
    lineGraph_foam(result_foam_df, selected_factories, selected_locations, from_year, to_year)

