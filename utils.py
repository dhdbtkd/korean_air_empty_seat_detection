import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO)

def log_error(error):
    logging.error(f"An error occurred: {error}")
