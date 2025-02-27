import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from modules.ml import performance_pred as p
from modules.ml import prediction


def show_PredictivePerformance():
    # Custom CSS to reduce header size and adjust layout.  Moved here to be within the function.
    st.markdown("""
    <style>
        .reportview-container .main .block-container {
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        .reportview-container .main {
            color: #333;
            background-color: #f0f2f6;
        }
        h1 {
            font-size: 40px !important;  /* Increased font size */
            margin-bottom: -1rem !important;
            margin-top: -3rem !important; /* Adjusted margin */
            font-weight: bold !important; /* Makes it bold */
        }
        .stSelectbox [data-baseweb="select"] {
            margin-top: 0 !important;
        }
        .stExpander {
            background-color: white !important;
            border-radius: 0.5rem !important;
            border: 1px solid #e0e0e0 !important;
        }
        .streamlit-expanderHeader {
            font-size: 1rem !important;
            padding: -1rem !important;
        }
        .streamlit-expanderContent {
            padding: 0.5rem !important;
        }
        .css-1d391kg {
            padding-top: 1rem !important;
        }
        .css-12oz5g7 {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }
        .css-1v0mbdj {
            padding-top: 0 !important;
        }
        .css-qrbaxs {
            font-size: 20px !important;
            min-height: 0.5rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title('Predictive Performance')

    # Get predictions for each target variable.
    # Note: For revenue, we now use 'Revenue ($)' so that the column exists in the data.
    result_vol_df = p.get_vol_prediction_for_6month('Production Volume (units)')
    result_rev_df = p.get_rev_prediction_for_6month('Revenue ($)')
    result_foam_df = p.get_foam_prediction_for_6month('Profit Margin (%)')

    # Define main menu options for the prediction targets.
    menu_options = [
         "Predicted Production Volume",
        "Predicted Revenue",
         "Predicted Profit Margin"
    ]

    # Create two columns: left for menu and filters, right for the graph/table content.
    col_left, col_right = st.columns([1.5, 3.5])

    with col_left:
        # Vertical menu at the top.
        selected = option_menu(
            menu_title="Menu",  
            options=menu_options,
            icons=['box-seam', 'currency-dollar', 'droplet-fill'],
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {
                    "padding": "25px!important",
                    "background-color": "transparent",
                    "margin-left": "-30px"
                },
                "icon": {"color": "var(--primary-color)", "font-size": "20px"},
                "nav-link": {
                    "font-size": "20px",  # Reduced text size
                    "text-align": "left",
                    "margin": "0px","margin-bottom": "0rem !important",
                    "--hover-color": "rgba(255, 255, 255, 0.1)"
                },
                "nav-link-selected": {"background-color": "var(--primary-color)", "color": "white"},
            }
        )
        st.markdown("<div style='margin-top: -100px;'></div>", unsafe_allow_html=True)

        # Spacer to push the filters lower in the left column.

        # Filters placed inside an expander.
        with st.expander("Filters", expanded=True):
            # Based on the selected option, choose the corresponding dataframe.
            if selected == "Predicted Revenue ($)":
                df = result_rev_df
            elif selected == "Predicted Production Volume":
                df = result_vol_df
            else:
                df = result_foam_df

            st.write("Select the time range:")
            factory_profit_df = result_rev_df  # Assuming result_rev_df contains the 'Month' column
            from_month, to_month = prediction.yearFilter(factory_profit_df)

            st.write("Select factories:")
            selected_factories = prediction.selectedFactories(df)

            st.write("Select locations:")
            selected_locations = prediction.selectedLocations(df)

    with col_right:
        # Display only one graph and its table based on the selected menu option.
        if selected == "Predicted Revenue":
            prediction.lineGraph_rev(result_rev_df, selected_factories, selected_locations, from_month, to_month)
        elif selected == "Predicted Profit Margin":
            prediction.lineGraph_foam(result_foam_df, selected_factories, selected_locations, from_month, to_month)
        elif selected == "Predicted Production Volume":
            prediction.lineGraph_vol(result_vol_df, selected_factories, selected_locations, from_month, to_month)
