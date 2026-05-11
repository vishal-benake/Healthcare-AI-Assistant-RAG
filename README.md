# Healthcare AI Assistant (RAG-Based System)

![Maintenance](https://img.shields.io/badge/Maintained%3F-under%20maintenance-orange.svg)

> **Note:** This repository is currently undergoing maintenance to improve document ingestion and fix directory pathing issues.

---

A production-style Retrieval-Augmented Generation (RAG) system for healthcare assistance.  
It retrieves relevant information from documents and generates grounded responses using a large language model.

---

## Features

- Multi-format document ingestion (PDF, TXT, DOCX, CSV, MD, XML)
- Retrieval-Augmented Generation (RAG) pipeline
- FAISS-based vector database for similarity search
- Sentence Transformer embeddings for semantic retrieval
- LLM-powered response generation using Groq API
- Web-based chat interface
- Source attribution for every response
- Confidence scoring (high, medium, low)
- Rule-based healthcare appointment system
- Structured JSON responses for safety and consistency

---

## System Architecture

User Query  
→ Flask Backend  
→ Query Router (RAG or Appointment System)  
→ FAISS Vector Search  
→ Context Retrieval  
→ LLM (Groq / LLaMA 3)  
→ Structured JSON Response  
→ Frontend UI

---

## Tech Stack

- Backend: Flask  
- Vector Database: FAISS  
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)  
- LLM: Groq (LLaMA 3)  
- Frontend: HTML, Bootstrap, JavaScript  
- Frameworks: LangChain  
- Language: Python 3.9+

---

## How It Works

### 1. Document Ingestion
Loads documents from the data directory and extracts text.

### 2. Text Splitting
Splits documents into smaller semantic chunks.

### 3. Embedding Generation
Converts chunks into vector embeddings using a transformer model.

### 4. Vector Storage
Stores embeddings in FAISS for fast similarity search.

### 5. Retrieval
Finds relevant document chunks based on user query.

### 6. Generation
LLM generates a response based only on retrieved context.

---

## Chat Features

- Real-time chat interface
- Typing animation for responses
- Source citations for answers
- Confidence scoring
- Appointment booking assistant

---

## Appointment System

Supports structured booking queries for:

- Cardiology
- Neurology
- Orthopedics

Example:

Book cardiology appointment on Monday

Response includes:
- Doctor name
- Available slots
- Structured output

---

## Installation

### Clone repository

```bash
git clone https://github.com/vishal-benake/healthcare-ai-assistance-RAG
cd healthcare-rag


Create virtual environment
python -m venv venv

Activate:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
Install dependencies
pip install -r requirements.txt
Set API key

Windows

set GROQ_API_KEY=your_api_key

Mac/Linux

export GROQ_API_KEY=your_api_key
Run application
python app.py
Open in browser
http://localhost:5000
API Endpoints
Health Check
GET /health

Response:

{
  "status": "ok"
}
Query Endpoint
POST /query

Request:

{
  "query": "What is diabetes?"
}

Response:

{
  "answer": "...",
  "confidence": "high",
  "sources": ["file.pdf"]
}
Example Output

User:
What are symptoms of diabetes?

Response:

Increased thirst
Frequent urination
Fatigue

Confidence: High
Sources: medical_data.pdf

Safety Features
Response restricted to retrieved context only
No hallucination policy enforced
Structured JSON outputs
Confidence scoring system
Prompt injection protection