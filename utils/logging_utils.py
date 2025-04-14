import logging
import os

def setup_logger(log_file=None):
    """Configure logging for the pipeline"""
    logger = logging.getLogger('ASD_Metagenomics')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

# Change this function name to match what's being imported
def get_logger():
    """Get the logger instance."""
    return logging.getLogger()
