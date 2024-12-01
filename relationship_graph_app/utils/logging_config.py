import logging
import sys
import os

def configure_logging():
    """Configure logging for the application"""
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Log to console
            logging.StreamHandler(sys.stdout),
            # Log to file
            logging.FileHandler(os.path.join(log_dir, 'app.log'), mode='a')
        ]
    )

# Optional: Add a method to get a logger for specific modules
def get_logger(name):
    """
    Get a logger for a specific module with default configuration
    """
    return logging.getLogger(name)
