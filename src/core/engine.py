import os
from src.core.embedder import Embedder
from src.core.llm_handler import LLMHandler
from src.core.tools import appointment_booking_tool
from src.utils.logger import get_logger
from src.utils.config import MAX_HISTORY
from src.data_handlers.ingestor import Ingestor

logger = get_logger(__name__)

class MedicalEngine:
    def __init__(self):
        self.embedder = Embedder()
        self.llm = LLMHandler()
        self.db = self.embedder.load_index()
        self.chat_history = [] # Local memory

    def boot_up(self):
        """
        Handles the ingestion process: 
        Parses data -> Creates Chunks -> Generates Embeddings -> Saves FAISS Index
        """
        try:
            logger.info("Starting system boot_up (Ingestion)...")
            from src.data_handlers.ingestor import Ingestor
            
            ingestor = Ingestor()
            chunks = ingestor.run()
            
            if not chunks:
                logger.error("No data found in data/ folder.")
                return False
                
            self.db = self.embedder.create_index(chunks)
        
            logger.info("Boot_up successful. FAISS index created.")
            return True
        except Exception as e:
            logger.error(f"Boot_up failed: {e}")
            return False

    def route_query(self, query):
        keywords = ["appointment", "book", "schedule", "slot", "consultation"]
        return "appointment" if any(k in query.lower() for k in keywords) else "rag"

    def query(self, user_query):
        # 1. Routing
        if self.route_query(user_query) == "appointment":
            return appointment_booking_tool(user_query)

        if not self.db:
            return {"answer": "Database not initialized.", "confidence": "low", "sources": []}

        try:
            # 2. Retrieval with Scores
            retrieved = self.db.similarity_search_with_score(user_query, k=4)
            
            # Filter weak matches (Score < 1.5)
            filtered_docs = [doc for doc, score in retrieved if score < 1.5]
            scores = [score for _, score in retrieved if score < 1.5]

            if not filtered_docs:
                return {"answer": "I could not find this in the documents.", "confidence": "low", "sources": []}

            # 3. Build Contexts
            context = "\n\n".join([d.page_content for d in filtered_docs])
            memory_ctx = "\n".join([f"{m['role']}: {m['content']}" for m in self.chat_history])

            # 4. Generate
            result = self.llm.ask(context, user_query, memory_ctx)
            
            # 5. Metadata & Confidence
            result['sources'] = list(set([os.path.basename(d.metadata.get('source', 'unknown')) for d in filtered_docs]))
            
            # Update Memory
            self.chat_history.append({"role": "user", "content": user_query})
            self.chat_history.append({"role": "assistant", "content": result['answer']})
            if len(self.chat_history) > MAX_HISTORY:
                self.chat_history = self.chat_history[-MAX_HISTORY:]

            return result

        except Exception as e:
            logger.error(f"Engine Error: {e}")
            return {"answer": "Error processing query.", "confidence": "low", "sources": []}
        
    def sync_new_data(self):
        """Scans for new files and updates the index incrementally."""
        logger.info("Scanning for new clinical documents...")
        ingestor = Ingestor()
        
        # 1. Get all current chunks from the data folder
        all_chunks = ingestor.run() 
        
        if not all_chunks:
            return

        # 2. Check if we have an existing DB
        if self.db is None:
            logger.info("Initializing new index...")
            self.db = self.embedder.create_index(all_chunks)
        else:
            self.db = self.embedder.create_index(all_chunks)
            
        logger.info("Database synchronized with latest data folder state.")