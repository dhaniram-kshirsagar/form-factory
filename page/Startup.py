import streamlit as st
from PIL import Image  # Import the Pillow library for image handling

def show_image():
    """Displays an image at its full size in the Streamlit app.

    Args:
        image_path (str): The path to the image file.
    """
    try:
        # Attempt to open the image using Pillow (PIL)
        image = Image.open('home.jpg')

        # Display the image with no size restrictions
        st.image(image, use_column_width=True) # Use full width

    except FileNotFoundError:
        st.error(f"Error: Image not found at {'home.jpg'}")
    except Exception as e:
        st.error(f"Error loading image: {e}")
