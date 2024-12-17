import streamlit as st
from pathlib import Path

def displayHome():
    image = Path(__file__).parent/'homescreen.jpg'
    st.image(image)
