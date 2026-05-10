import os
import html
import logging
import xml.etree.ElementTree as ET

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader
)

from src.config import DATA_DIR, SUPPORTED_EXTENSIONS

documents = []

def enrich_metadata(doc, file_path, file_name):

    doc.metadata = doc.metadata or {}

    doc.metadata.update({
        "source": file_path,
        "file_name": file_name,
        "file_type": os.path.splitext(file_name)[1].replace(".", "")
    })

    return doc


def load_documents():

    global documents

    print("Starting document ingestion...\n")

    for root, dirs, files in os.walk(DATA_DIR):

        for file in files:

            file_path = os.path.join(root, file)

            if not file.lower().endswith(SUPPORTED_EXTENSIONS):
                continue

            try:

                loaded_docs = []

                if file.endswith(".pdf"):
                    loaded_docs = PyPDFLoader(file_path).load()

                elif file.endswith(".txt"):
                    loaded_docs = TextLoader(file_path, encoding="utf-8").load()

                elif file.endswith(".csv"):
                    loaded_docs = CSVLoader(file_path).load()

                elif file.endswith(".docx"):
                    loaded_docs = Docx2txtLoader(file_path).load()

                elif file.endswith(".md"):
                    loaded_docs = UnstructuredMarkdownLoader(file_path).load()

                elif file.endswith(".xml"):

                    tree = ET.parse(file_path)
                    root_xml = tree.getroot()

                    xml_text = " ".join(
                        text.strip()
                        for text in root_xml.itertext()
                        if text.strip()
                    )

                    xml_text = html.unescape(xml_text)

                    loaded_docs = [
                        Document(
                            page_content=xml_text,
                            metadata={
                                "source": file_path,
                                "file_name": file,
                                "file_type": "xml"
                            }
                        )
                    ]

                documents.extend([
                    enrich_metadata(doc, file_path, file)
                    for doc in loaded_docs
                ])

                logging.info(f"Loaded: {file_path}")
                print(f"Loaded: {file_path}")

            except Exception as e:
                logging.error(f"Error loading {file_path}: {str(e)}")
                print(f"Error loading: {file_path} -> {str(e)}")

    print(len(documents))
    return documents