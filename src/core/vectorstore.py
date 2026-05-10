import os
from langchain_community.vectorstores import FAISS
from src.config import FAISS_PATH

def create_vectorstore(texts, embedding_model, metadatas):

    vectorstore = FAISS.from_texts(
        texts=texts,
        embedding=embedding_model,
        metadatas=metadatas
    )

    os.makedirs(FAISS_PATH, exist_ok=True)
    vectorstore.save_local(FAISS_PATH)

    return vectorstore


def load_vectorstore(embedding_model):

    index_file = os.path.join(FAISS_PATH, "index.faiss")

    if not os.path.exists(index_file):
        return None

    db = FAISS.load_local(
        FAISS_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    return db