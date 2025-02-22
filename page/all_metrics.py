import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

# Custom CSS to improve appearance in both light and dark themes
css = """
<style>
    .stPlotlyChart {
        border-radius: 0.5rem;
        #box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .stMetric {
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .menu-container {
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .content-container {
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin-bottom: 1rem;
    }
    /* Ensure text is visible in both light and dark modes */
    .stApp h1, .stApp h2, .stApp h3, .stApp label, .stApp .stMetric, .stSelectbox label, .stDateInput label {
        color: var(--text-color) !important;
    }
    .stMetric [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }
    /* Dark mode */
    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #1e1e1e;
            --secondary-background-color: #2d2d2d;
            --primary-color: #6d9eeb;
        }
    }
    /* Fix for graph container height */
    .stPlotlyChart > div {
        height: 600px !important;
    }
</style>
"""

from pathlib import Path

DATA_FILE = Path(__file__).parent.parent/"modules/data/large-data/FoamFactory_V2_27K.csv"

def show_allmetrics():  #No need to call it but let's fix its position

    # Load data
    @st.cache_data
    def load_data():
        try:
            df = pd.read_csv(DATA_FILE)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return pd.DataFrame()

    df = load_data()

    st.markdown(css, unsafe_allow_html=True)

    if df.empty:
        st.error("No data available. Please check your CSV file.")
        st.stop()

    # Main layout
    menu_col, content_col = st.columns([1, 3])

    with menu_col:
        st.markdown('<div class="menu-container">', unsafe_allow_html=True)
        st.title("Dashboard")
        
        # Set default date range to the most recent year
        end_date = df['Date'].max()
        start_date = end_date - timedelta(days=365)
        
        date_range = st.date_input("Select Date Range", [start_date, end_date], key="date_range")
        factory = st.selectbox("Select Factory", df['Factory'].unique())
        
        selected_dashboard = option_menu(
            "Selection Menu",
            ["Production Efficiency", "Downtime Analysis", "Quality Control", "Operator Performance", "Environmental Impact", "Cost & Profitability"],
            icons=['graph-up', 'clock-history', 'check-circle', 'people', 'gear', 'currency-dollar'],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent", "height": "725px"},
                "icon": {"color": "var(--primary-color)", "font-size": "20px"}, 
                "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "rgba(255, 255, 255, 0.1)"},
                "nav-link-selected": {"background-color": "var(--primary-color)", "color": "white"},
            }
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Filter data
    filtered_df = df[(df['Date'].dt.date >= date_range[0]) & 
                    (df['Date'].dt.date <= date_range[1]) & 
                    (df['Factory'] == factory)]

    # Resample data to monthly frequency
    monthly_df = filtered_df.set_index('Date').resample('MS').agg({
        'Production Volume (units)': 'sum',
        'Batch Quality (Pass %)': 'mean',
        'Cycle Time (minutes)': 'mean',
        'Machine Downtime (hours)': 'sum',
        'Defect Rate (%)': 'mean',
        'Breakdowns (count)': 'sum',
        'Operator Experience (years)': 'mean',
        'Safety Incidents (count)': 'sum',
        'Absenteeism Rate (%)': 'mean',
        'Energy Consumption (kWh)': 'sum',
        'CO2 Emissions (kg)': 'sum',
        'Waste Generated (kg)': 'sum',
        'Water Usage (liters)': 'sum',
        'Revenue ($)': 'sum',
        'Cost of Downtime ($)': 'sum',
        'Profit Margin (%)': 'mean'
    }).reset_index()

    def create_metric_card(title, value, delta=None):
        if delta:
            return st.metric(title, value, delta)
        return st.metric(title, value)

    def get_plot_theme():
        return "plotly_white" if st.get_option("theme.base") == "light" else "plotly_dark"

    def create_chart(df, x, y, title):
        fig = px.line(df, x=x, y=y, title=title)
        fig.update_traces(line=dict(width=3))
        fig.update_layout(
            template=get_plot_theme(),
            height=650,
            xaxis_title="Months",
            yaxis_title=y,
            hovermode="x unified",
            xaxis=dict(
                tickformat="%b %Y",
                tickangle=45,
                tickmode='auto',
                nticks=20,
            ),
            yaxis=dict(
                tickformat=",",
            ),
            margin=dict(l=50, r=50, t=50, b=50),
        )
        return fig

    with content_col:
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.title(f"{selected_dashboard} - {factory}")

        if selected_dashboard == "Production Efficiency":
            col1, col2, col3 = st.columns(3)
            with col1:
                create_metric_card("Total Production", f"{monthly_df['Production Volume (units)'].sum():,.0f} units")
            with col2:
                avg_quality = monthly_df['Batch Quality (Pass %)'].mean()
                create_metric_card("Average Batch Quality", f"{avg_quality:.2f}%")
            with col3:
                avg_cycle_time = monthly_df['Cycle Time (minutes)'].mean()
                create_metric_card("Average Cycle Time", f"{avg_cycle_time:.2f} min")

            fig_production = create_chart(monthly_df, 'Date', 'Production Volume (units)', 'Monthly Production Volume Trend')
            st.plotly_chart(fig_production, use_container_width=True, config={'displayModeBar': False})

        elif selected_dashboard == "Downtime Analysis":
            col1, col2 = st.columns(2)
            with col1:
                total_downtime = monthly_df['Machine Downtime (hours)'].sum()
                create_metric_card("Total Downtime", f"{total_downtime:,.2f} hours")
            with col2:
                avg_downtime = monthly_df['Machine Downtime (hours)'].mean()
                create_metric_card("Average Monthly Downtime", f"{avg_downtime:.2f} hours")

            fig_downtime = create_chart(monthly_df, 'Date', 'Machine Downtime (hours)', 'Monthly Downtime Trend')
            st.plotly_chart(fig_downtime, use_container_width=True, config={'displayModeBar': False})

        elif selected_dashboard == "Quality Control":
            col1, col2 = st.columns(2)
            with col1:
                avg_defect_rate = monthly_df['Defect Rate (%)'].mean()
                create_metric_card("Average Defect Rate", f"{avg_defect_rate:.2f}%")
            with col2:
                total_breakdowns = monthly_df['Breakdowns (count)'].sum()
                create_metric_card("Total Breakdowns", f"{total_breakdowns:,.0f}")

            fig_quality = create_chart(monthly_df, 'Date', 'Batch Quality (Pass %)', 'Monthly Batch Quality Trend')
            st.plotly_chart(fig_quality, use_container_width=True, config={'displayModeBar': False})

        elif selected_dashboard == "Operator Performance":
            col1, col2 = st.columns(2)
            with col1:
                avg_operator_experience = monthly_df['Operator Experience (years)'].mean()
                create_metric_card("Average Operator Experience", f"{avg_operator_experience:.2f} years")
            with col2:
                total_safety_incidents = monthly_df['Safety Incidents (count)'].sum()
                create_metric_card("Total Safety Incidents", f"{total_safety_incidents:,.0f}")

            fig_operator = go.Figure()
            fig_operator.add_trace(go.Scatter(x=monthly_df['Date'], y=monthly_df['Absenteeism Rate (%)'], name='Absenteeism Rate', line=dict(width=3)))
            fig_operator.add_trace(go.Scatter(x=monthly_df['Date'], y=monthly_df['Operator Experience (years)'], name='Operator Experience', line=dict(width=3)))
            fig_operator.update_layout(
                title='Monthly Operator Performance Trends',
                template=get_plot_theme(),
                height=650,
                xaxis_title="Months",
                yaxis_title="Value",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_operator, use_container_width=True, config={'displayModeBar': False})

        elif selected_dashboard == "Environmental Impact":
            col1, col2, col3 = st.columns(3)
            with col1:
                total_energy = monthly_df['Energy Consumption (kWh)'].sum()
                create_metric_card("Total Energy Consumption", f"{total_energy:,.0f} kWh")
            with col2:
                total_water = monthly_df['Water Usage (liters)'].sum() / 1000  # Convert to kiloliters
                create_metric_card("Total Water Usage", f"{total_water:,.2f} kL")
            with col3:
                total_waste = monthly_df['Waste Generated (kg)'].sum()
                create_metric_card("Total Waste Generated", f"{total_waste:,.0f} kg")

            fig_env = go.Figure()
            fig_env.add_trace(go.Scatter(x=monthly_df['Date'], y=monthly_df['Energy Consumption (kWh)'], name='Energy Consumption', line=dict(width=3)))
            fig_env.add_trace(go.Scatter(x=monthly_df['Date'], y=monthly_df['CO2 Emissions (kg)'], name='CO2 Emissions', line=dict(width=3)))
            fig_env.add_trace(go.Scatter(x=monthly_df['Date'], y=monthly_df['Waste Generated (kg)'], name='Waste Generated', line=dict(width=3)))
            fig_env.update_layout(
                title='Monthly Environmental Impact Trends',
                template=get_plot_theme(),
                height=800,
                xaxis_title="Months",
                yaxis_title="Value",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_env, use_container_width=True, config={'displayModeBar': False})

        elif selected_dashboard == "Cost & Profitability":
            col1, col2, col3 = st.columns(3)
            with col1:
                total_revenue = monthly_df['Revenue ($)'].sum() / 1_000_000  # Convert to millions
                create_metric_card("Total Revenue", f"${total_revenue:,.2f}M")
            with col2:
                total_downtime_cost = monthly_df['Cost of Downtime ($)'].sum() / 1_000_000  # Convert to millions
                create_metric_card("Total Cost of Downtime", f"${total_downtime_cost:,.2f}M")
            with col3:
                avg_profit_margin = monthly_df['Profit Margin (%)'].mean()
                create_metric_card("Average Profit Margin", f"{avg_profit_margin:.2f}%")

            fig_finance = go.Figure()
            fig_finance.add_trace(go.Scatter(x=monthly_df['Date'], y=monthly_df['Revenue ($)'] / 1_000_000, name='Revenue (Millions)', line=dict(width=3)))
            fig_finance.add_trace(go.Scatter(x=monthly_df['Date'], y=monthly_df['Cost of Downtime ($)'] / 1_000_000, name='Cost of Downtime (Millions)', line=dict(width=3)))
            fig_finance.update_layout(
                title='Monthly Revenue vs Cost of Downtime Trend',
                template=get_plot_theme(),
                height=650,
                xaxis_title="Months",
                yaxis_title="Value (Millions $)",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_finance, use_container_width=True, config={'displayModeBar': False})

        st.markdown('</div>', unsafe_allow_html=True)

# show_allmetrics()  #Now calling the function