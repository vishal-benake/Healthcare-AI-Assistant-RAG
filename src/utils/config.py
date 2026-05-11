import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
FAISS_INDEX_DIR = os.path.join(BASE_DIR, "faiss_index")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Embedding Config
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

DEVICE = "cpu" 

# Memory Config
MAX_HISTORY = 6

CHUNK_SIZE = 2000      # Larger chunks = fewer total embeddings to generate
CHUNK_OVERLAP = 100

for path in [DATA_DIR, FAISS_INDEX_DIR, LOG_DIR]:
    os.makedirs(path, exist_ok=True)