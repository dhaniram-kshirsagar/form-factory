# import streamlit as st
# # import pandas as pd

# import os
# from dotenv import load_dotenv


# # Get the OpenAI API key
# # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # # Check if the key is loaded
# # if OPENAI_API_KEY is None:
# #     raise ValueError("OPENAI_API_KEY environment variable not set. Please create a .env file with OPENAI_API_KEY=<your_key>.")
# # else:
# #     print("OpenAI API key loaded successfully.")

# # from modules.data import data
# #from modules.chatbot import chatbot
# from modules.metrics import metrics as m

# # Set the title and favicon that appear in the Browser's tab bar.
# st.set_page_config(
#     page_title='Foam Factories',
#     page_icon=':factory:', # This is an emoji shortcode. Could be a URL too.
#     layout='wide',
# )

# # Load environment variables from .env file
# st.session_state.OPENAI_API_KEY = None

# if st.session_state.OPENAI_API_KEY is None:
#     load_dotenv()
#     st.session_state.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#     print("OpenAI API key loaded successfully.")

# # -----------------------------------------------------------------------------
# # Declare some useful functions.


# #factories_df = data.getFactoryComplexDataProfit()
# # factories_df['Year'] = pd.DatetimeIndex(factories_df['date']).year
# # factories_df['Month'] = pd.DatetimeIndex(factories_df['date']).month
# # -----------------------------------------------------------------------------
# # Draw the actual page

# # Set the title that appears at the top of the page.
# '''
# # :factory: Factory Status

# '''

# # Add some spacing
# ''

# # m.metricsPage(factories_df)

# m.metricsPage()


# # def click_button():
# #     st.session_state.clicked = True
# #     chatbot.open_chatbot()

# # from streamlit_float import *

# # # Float feature initialization
# # float_init()

# # # Container with expand/collapse button
# # button_container = st.container()
# # with button_container:
# #     st.button(":material/robot_2:", on_click=click_button, type="primary")

# # button_css = float_css_helper(width="2.2rem", right="2rem", bottom="0rem", transition=0)

# # button_container.float(button_css)

import streamlit as st
# import pandas as pd

import os
from dotenv import load_dotenv

from streamlit_navigation_bar import st_navbar
import page as pg

# Get the OpenAI API key
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Check if the key is loaded
# if OPENAI_API_KEY is None:
#     raise ValueError("OPENAI_API_KEY environment variable not set. Please create a .env file with OPENAI_API_KEY=<your_key>.")
# else:
#     print("OpenAI API key loaded successfully.")

# from modules.data import data
#from modules.chatbot import chatbot


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    #page_title='Foam Factories',
    #page_icon=':factory:', # This is an emoji shortcode. Could be a URL too.
    layout='wide',
    initial_sidebar_state="collapsed"
)

# Load environment variables from .env file
st.session_state.OPENAI_API_KEY = None

if st.session_state.OPENAI_API_KEY is None:
    load_dotenv()
    st.session_state.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    print("OpenAI API key loaded successfully.")

#st.set_page_config(initial_sidebar_state="collapsed")

pages = ["Home", "Performance","Factory Bot", "Factory Astro", "Predictive Performance", "Current Performance"]
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, "no_bg_logo.svg")
#urls = {"GitHub": "https://github.com/gabrieltempass/streamlit-navigation-bar"}
styles = {
    "nav": {
        "background-color": "white",
        "justify-content": "left",
        "font-size":"12px"
    },
    "img": {
        "padding-right": "20px",
        "width": "75px",
        "height": "75px"
    },
    "span": {
        "color": "black",
        "padding": "14px",
    },
    "active": {
        "background-color": "red",
        "color": "var(--text-color)",
        "font-weight": "light",
        "font-size":"12px",
        "padding": "14px",
    }
}
options = {
    "show_menu": True,
    "show_sidebar": True,
    "use_padding": True
}

page = st_navbar(
    pages,
    logo_path=logo_path,
    #urls=urls,
    styles=styles,
    options=options,
)

functions = {
    "Home": pg.show_image,
    "Performance": pg.show_page,
    "Factory Bot": pg.show_factorybot,
    "Factory Astro":pg.Show_Factoryastro,
    "Predictive Performance": pg.show_PredictivePerformance,
    "Current Performance": pg.show_currentPerformance,
    
    
}

go_to = functions.get(page)
if go_to:
    go_to()

# -----------------------------------------------------------------------------
# Declare some useful functions.


#factories_df = data.getFactoryComplexDataProfit()
# factories_df['Year'] = pd.DatetimeIndex(factories_df['date']).year
# factories_df['Month'] = pd.DatetimeIndex(factories_df['date']).month
# -----------------------------------------------------------------------------
# Draw the actual page

# Add logo to the sidebar
# st.sidebar.image("no_bg_logo.png", width=200)

# # Set the title that appears at the top of the page.
# col1, col2, col3 = st.columns([1, 2, 1])

# with col2:
#     st.image("no_bg_logo.png", width=400)

'''

'''

# Add some spacing
''

# m.metricsPage(factories_df)

#m.metricsPage()


# def click_button():
#     st.session_state.clicked = True
#     chatbot.open_chatbot()

# from streamlit_float import *

# # Float feature initialization
# float_init()

# # Container with expand/collapse button
# button_container = st.container()
# with button_container:
#     st.button(":material/robot_2:", on_click=click_button, type="primary")

# button_css = float_css_helper(width="2.2rem", right="2rem", bottom="0rem", transition=0)

# button_container.float(button_css)
