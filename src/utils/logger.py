import logging
import os
from datetime import datetime
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

# 1. Setup Timestamped Directory
# Format: logs/run_05_11_2026_12_30_45/
RUN_ID = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
LOG_FOLDER = os.path.join(os.getcwd(), "logs", f"run_{RUN_ID}")
os.makedirs(LOG_FOLDER, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_FOLDER, "clinical_session.log")

def get_logger(name):
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if logger is called multiple times
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # File Handler 
        file_handler = logging.FileHandler(LOG_FILE_PATH)
        formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        
        # Rich Handler (Beautiful terminal output with colors)
        rich_handler = RichHandler(rich_tracebacks=True, markup=True)

        logger.addHandler(file_handler)
        logger.addHandler(rich_handler)
        
    return logger

# 2. Professional Progress Context Manager
def get_progress_bar():
    """Returns a pre-configured progress bar for long-running tasks."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    )