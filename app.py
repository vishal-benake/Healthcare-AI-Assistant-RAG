from flask import Flask, request, jsonify, render_template

from src.logger import setup_logging
from src.core.ingestion import load_documents
from src.core.splitter import split_documents
from src.core.embeddings import get_embedding_model
from src.core.vectorstore import create_vectorstore, load_vectorstore
from src.rag.pipeline import healthcare_rag
from langchain_groq import ChatGroq

setup_logging()

app = Flask(__name__)

# =========================
# LOAD + BUILD PIPELINE
# =========================

documents = load_documents()
chunks = split_documents(documents)

embedding_model, device = get_embedding_model()

texts = [c.page_content for c in chunks]
metadatas = [c.metadata for c in chunks]

db = load_vectorstore(embedding_model)

if db is None:
    vectorstore = create_vectorstore(texts, embedding_model, metadatas)
    db = vectorstore

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.2,
    max_tokens=1024,
    timeout=60,
    max_retries=3
)

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/query", methods=["POST"])
def query():

    try:
        data = request.get_json()

        if not data or "query" not in data:
            return jsonify({"error": "query is required"}), 400

        user_query = data["query"]

        if not user_query.strip():
            return jsonify({"error": "empty query"}), 400

        result = healthcare_rag(user_query, db, llm)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": "internal server error",
            "message": str(e)
        }), 500


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )