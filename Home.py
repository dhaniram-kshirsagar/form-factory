import streamlit as st
import pandas as pd

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the key is loaded
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please create a .env file with OPENAI_API_KEY=<your_key>.")
else:
    print("OpenAI API key loaded successfully.")

from modules.data import data
from modules.chatbot import chatbot
from modules.metrics import metrics as m

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Foam Factories',
    page_icon=':factory:', # This is an emoji shortcode. Could be a URL too.
    layout='wide',
)


# -----------------------------------------------------------------------------
# Declare some useful functions.


factories_df = data.getFactoryComplexDataProfit()
factories_df['Year'] = pd.DatetimeIndex(factories_df['date']).year
factories_df['Month'] = pd.DatetimeIndex(factories_df['date']).month
# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :factory: Factory Status

'''

# Add some spacing
''

m.metricsPage(factories_df)


def click_button():
    st.session_state.clicked = True
    chatbot.open_chatbot()

from streamlit_float import *

# Float feature initialization
float_init()

# Container with expand/collapse button
button_container = st.container()
with button_container:
    st.button(":material/robot_2:", on_click=click_button, type="primary")

button_css = float_css_helper(width="2.2rem", right="2rem", bottom="0rem", transition=0)

button_container.float(button_css)
