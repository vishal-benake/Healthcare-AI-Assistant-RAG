# Healthcare AI Assistant (RAG-Based System)

![Maintenance](https://img.shields.io/badge/Maintained%3F-under%20maintenance-orange.svg)

> **Note:** This repository is currently undergoing maintenance to improve document ingestion and fix directory pathing issues.

---


A professional-grade Retrieval-Augmented Generation (RAG) system designed to provide clinical insights by indexing medical documents (PDF, XML, CSV, TXT) and querying them using Large Language Models.

##  Key Features
*   **Multi-Format Ingestion:** Seamlessly processes PDFs, Clinical XMLs, CSV data, and raw text.
*   **Hybrid Architecture:** Separate data pipeline for high-performance vectorization and a Flask API for real-time interaction.
*   **Optimized Retrieval:** Uses `RecursiveCharacterTextSplitter` with tuned chunking (2000/100) for fast, context-aware medical querying.
*   **Vector Search:** Powered by FAISS and HuggingFace Embeddings (`all-MiniLM-L6-v2`).
*   **Background Sync:** (Optional) Integrated scheduler to monitor data folders for new clinical records.

---

##  Project Structure
```text
Healthcare-AI-Assistant-RAG/
├── data/               # Drop clinical PDFs/XMLs/CSVs here
├── faiss_index/        # Generated vector database (Auto-created)
├── src/
│   ├── api/            # Flask blueprints and routes
│   ├── core/           # RAG Engine, Embedder, and LLM logic
│   ├── data_handlers/  # Ingestor and document parsers
│   └── utils/          # Configuration and logging
├── static/             # Frontend CSS/JS
├── templates/          # HTML Interface
├── app.py              # Main Web Server
├── ingest_data.py      # Manual Data Pipeline script
└── requirements.txt    # Project dependencies
```

---

## Installation & Setup

Clone & Environment
```bash
git clone https://github.com/vishal-benake/Healthcare-AI-Assistant-RAG.git
```
```bash
cd healthcare-rag
```
```bash
python -m venv myenv
```
```bash
source myenv/bin/activate  # Windows: myenv\Scripts\activate
```


## Install Dependencies
```bash
pip install -r requirements.txt
```

## Data Ingestion
Place your medical documents in the /data folder, then run the pipeline to vectorize the content:

```bash
python ingest_data.py
```

## Run the Application
```bash
python app.py
```

Visit http://localhost:5000 in your browser.

## Configuration
Adjust performance settings in src/utils/config.py:

CHUNK_SIZE: 2000 (Optimized for speed)

CHUNK_OVERLAP: 100

DEVICE: 'cpu' (Change to 'cuda' for GPU acceleration)

---

Before running anything, ensure your virtual environment is active and all libraries are present.

Activate Environment:

```bash
    myenv\Scripts\activate
```
Install Requirements: (If you haven't already)

```bash
    pip install -r requirements.txt
```

---

##  The Data Ingestion (Manual)
This is where the "Brain" is built. Do this whenever you add new files to the `data/` folder.

1.  **Place Files:** Drop your PDFs, CSVs, or XMLs into the `data/` folder.
2.  **Run Pipeline:**
    ```bash
    python ingest_data.py
    ```
3.  **What to watch for:** You should see a progress bar (e.g., `103/103`). Once it finishes, a new folder named `faiss_index` will appear in your project. **If this folder exists, your AI has "memory."**

---

## Launching the Interface
Now that the database is ready, start the Flask server.

1.  **Run App:**
    ```bash
    python app.py
    ```
2.  **Access:** Open your browser and go to:
    `[http://127.0.0.1:5000](http://127.0.0.1:5000)`

---

##  How to use the Assistant
Once the frontend loads, you can interact with it in three ways:

*   **General Greetings:** Type "Hi" or "Hello." The system will respond using the LLM's internal knowledge.
*   **Medical Queries:** Ask specific questions based on the files you uploaded (e.g., *"What are the symptoms mentioned in the latest patient report?"* or *"Summarize the treatment plan from the XML data."*).
*   **Live Sync:** If you add a file while `app.py` is running, wait about 60 seconds. The **Background Scheduler** we set up will automatically detect it and update the "brain" without you needing to restart the server.

---

## Troubleshooting Common Issues

| Issue | Solution |
| :--- | :--- |
| **"Database not initialized"** | You skipped Step 2. Run `python ingest_data.py` first. |
| **"ModuleNotFoundError"** | You are likely not in your virtual environment (`myenv`). |
| **System is slow** | Close Chrome tabs or other heavy apps. Embedding 1500+ chunks takes significant CPU power. |
| **Old data appearing** | Delete the `faiss_index` folder and run `python ingest_data.py` again to do a "Fresh Install" of your knowledge. |