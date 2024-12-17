import streamlit as st
import pandas as pd
import math
from pathlib import Path


import openai
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

from modules.data import data
from modules.chatbot import chatbot
from modules.metrics import metrics as m

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Foam Factories',
    page_icon=':factory:', # This is an emoji shortcode. Could be a URL too.
    layout='wide',
)


st.header('🤖  Foram Factories')

# page = 'Home'
# # Sidebar for navigation 
# st.sidebar.title('Navigation') 
# page = st.sidebar.selectbox( 'Select a page:', ('Home', 'Performance Section', 'Metrics Section', 'Profile Section') )

# -----------------------------------------------------------------------------
# Declare some useful functions.


factories_df = data.getFactoryDataProfit()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :factory: Foam Factory Dashboard

Analysis of foram factory performance and maintenance data.
'''

# Add some spacing
''
''


''
''
''

m.metricsPage(factories_df)

# if page == 'Home':
#     h.displayHome()
# elif page == 'Performance Section': 
#     st.title('Performance Dashboard')
#     p.performancePage(gdp_df)
# elif page == 'Metrics Section': 
#     st.title('Metrics Section')
#     m.metricsPage(factories_df)  

def click_button():
    st.session_state.clicked = True
    chatbot.open_chatbot()

''

from streamlit_float import *

# Float feature initialization
float_init()

# Container with expand/collapse button
button_container = st.container()
with button_container:
    st.button(":material/robot_2:", on_click=click_button, type="primary")

button_css = float_css_helper(width="2.2rem", right="2rem", bottom="0rem", transition=0)

button_container.float(button_css)
