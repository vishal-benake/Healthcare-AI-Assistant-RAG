# DATA_DIR = "data"
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

SUPPORTED_EXTENSIONS = (
    ".pdf",
    ".txt",
    ".csv",
    ".docx",
    ".md",
    ".xml"
)

FAISS_PATH = "faiss_index"