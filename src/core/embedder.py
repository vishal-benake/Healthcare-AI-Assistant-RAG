from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.utils.config import EMBEDDING_MODEL, FAISS_INDEX_DIR, DEVICE
import os

class Embedder:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': DEVICE} # Uses GPU if configured
        )

    def load_index(self):
        if os.path.exists(os.path.join(FAISS_INDEX_DIR, "index.faiss")):
            return FAISS.load_local(FAISS_INDEX_DIR, self.embeddings, allow_dangerous_deserialization=True)
        return None

    def create_index(self, chunks):
        db = FAISS.from_documents(chunks, self.embeddings)
        db.save_local(FAISS_INDEX_DIR)
        return db