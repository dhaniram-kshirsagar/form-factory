"""
Error Handling and Logging Utilities

This module provides centralized error handling and logging functionality
for the telecom churn prediction system.
"""

import logging
from functools import wraps
import streamlit as st


def setup_logging():
    """
    Initialize logging configuration

    Sets up basic logging configuration with:
    - INFO level logging
    - Timestamp format
    - Output to app.log file
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='app.log'
    )


def handle_errors(func):
    """
    Decorator for error handling

    Args:
        func: The function to wrap with error handling

    Returns:
        The wrapped function that handles errors and logs them

    This decorator catches exceptions, logs them, and displays a user-friendly
    error message in the Streamlit interface.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f'Error in {func.__name__}: {e}', exc_info=True)
            st.error(f'An error occurred in {func.__name__}. Please check the logs for more details.')
    return wrapper
