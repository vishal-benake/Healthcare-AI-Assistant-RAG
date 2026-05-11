import os
# from langchain.docstore.document import Document
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.data_handlers.xml_parser import parse_xml
from src.data_handlers.csv_handler import load_csv_text
from src.utils.config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from src.utils.logger import get_logger

logger = get_logger(__name__)

class Ingestor:
    def run(self):
        docs = []
        for root, _, files in os.walk(DATA_DIR):
            for file in files:
                path = os.path.join(root, file)
                content = None
                if file.endswith(".xml"):
                    content = parse_xml(path)
                elif file.endswith(".csv"):
                    content = load_csv_text(path)
                
                if content:
                    docs.append(Document(page_content=content, metadata={"source": file}))
        
        if not docs:
            logger.error("No data found to ingest!")
            return []

        splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        return splitter.split_documents(docs)