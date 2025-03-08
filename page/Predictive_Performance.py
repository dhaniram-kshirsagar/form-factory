import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from modules.ml import performance_pred as p
from modules.ml import prediction
import copy


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

    # Initialize session state for categorical filters if not exists
    if 'rev_categorical_filters' not in st.session_state:
        st.session_state.rev_categorical_filters = {}
    if 'vol_categorical_filters' not in st.session_state:
        st.session_state.vol_categorical_filters = {}
    if 'prof_categorical_filters' not in st.session_state:
        st.session_state.prof_categorical_filters = {}
        
    # Get predictions for each target variable with applied filters
    # Note: For revenue, we now use 'Revenue ($)' so that the column exists in the data.
    result_vol_df = p.get_vol_prediction_for_6month('Production Volume (units)', st.session_state.vol_categorical_filters)
    result_rev_df = p.get_rev_prediction_for_6month('Revenue ($)', st.session_state.rev_categorical_filters)
    result_profmargin_df = p.get_foam_prediction_for_6month('Profit Margin (%)', st.session_state.prof_categorical_filters)

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
            # Based on the selected option, choose the corresponding dataframe and model name
            if selected == "Predicted Revenue":
                df = result_rev_df
                model_name = 'revenue_model'
                categorical_filters = st.session_state.rev_categorical_filters
            elif selected == "Predicted Production Volume":
                df = result_vol_df
                model_name = 'production_volume_model'
                categorical_filters = st.session_state.vol_categorical_filters
            else:  # Profit Margin
                df = result_profmargin_df
                model_name = 'profit_margin_model'
                categorical_filters = st.session_state.prof_categorical_filters

            st.write("Select the time range:")
            from_month, to_month = prediction.yearFilter(df)

            st.write("Select factories:")
            selected_factories = prediction.selectedFactories(df)
            
            # Get categorical feature options for the selected model
            feature_options = p.get_categorical_feature_options()
            
            # Display categorical feature filters based on the selected model
            st.write("Categorical Feature Filters:")
            
            # Create a container for categorical filters with some spacing
            cat_filter_container = st.container()
            
            with cat_filter_container:
                # Define callback function for when a filter changes
                def on_filter_change():
                    # Update the appropriate session state
                    if model_name == 'revenue_model':
                        st.session_state.rev_categorical_filters = copy.deepcopy(categorical_filters)
                    elif model_name == 'production_volume_model':
                        st.session_state.vol_categorical_filters = copy.deepcopy(categorical_filters)
                    else:  # profit_margin_model
                        st.session_state.prof_categorical_filters = copy.deepcopy(categorical_filters)
                    
                # Add categorical feature filters based on the selected model
                if model_name in feature_options:
                    for feature, options in feature_options[model_name].items():
                        # Convert numeric options to strings with descriptive labels
                        display_options = {}
                        for opt in options:
                            if feature == 'Product Category':
                                display_options[f"Category {opt}"] = opt
                            elif feature == 'Machine Type':
                                display_options[f"Type {opt}"] = opt
                            elif feature == 'Supplier':
                                display_options[f"Supplier {opt}"] = opt
                            elif feature == 'Raw Material Quality':
                                quality_labels = {0: "Low", 1: "Medium", 2: "High"}
                                display_options[quality_labels.get(opt, f"Quality {opt}")] = opt
                            else:
                                display_options[f"Option {opt}"] = opt
                        
                        # Get current value from session state if it exists
                        current_value = None
                        if feature in categorical_filters:
                            current_value = categorical_filters[feature]
                            # Find the display label for the current value
                            current_label = next((label for label, val in display_options.items() 
                                                if val == current_value), None)
                            if current_label:
                                current_index = list(display_options.keys()).index(current_label)
                            else:
                                current_index = 0
                        else:
                            current_index = 0
                        
                        # Create a selectbox for each categorical feature with on_change callback
                        selected_option_label = st.selectbox(
                            f"Select {feature}:",
                            options=list(display_options.keys()),
                            index=current_index,
                            key=f"{model_name}_{feature}",
                            on_change=on_filter_change
                        )
                        
                        # Update the categorical filters with the selected value
                        selected_value = display_options[selected_option_label]
                        categorical_filters[feature] = selected_value

    with col_right:
        # Display only one graph and its table based on the selected menu option.
        if selected == "Predicted Revenue":
            prediction.lineGraph_rev(result_rev_df, selected_factories, from_month, to_month)
        elif selected == "Predicted Production Volume":
            prediction.lineGraph_vol(result_vol_df, selected_factories, from_month, to_month)
        elif selected == "Predicted Profit Margin":
            prediction.lineGraph_prof(result_profmargin_df, selected_factories, from_month, to_month)
