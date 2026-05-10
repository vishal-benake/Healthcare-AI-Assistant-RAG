import logging
import os
import sys

def setup_logging():
    os.makedirs("logs", exist_ok=True)

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/rag.log"),
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )

    logging.info("Logging system initialized.")