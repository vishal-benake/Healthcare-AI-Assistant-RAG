import pandas as pd
from src.utils.logger import get_logger

logger = get_logger(__name__)

def load_csv_text(file_path):
    try:
       
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading CSV {file_path}: {e}")
        return None