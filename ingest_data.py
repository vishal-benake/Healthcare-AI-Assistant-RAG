import os
import sys
from src.core.engine import MedicalEngine

def run_pipeline():
    print("⚕️  MedAI | Data Processing Pipeline")
    print("------------------------------------")
    
    # Initialize the engine
    # We call boot_up which triggers the Ingestor and Embedder
    engine = MedicalEngine()
    
    print("Scanning 'data/' folder for documents...")
    
    success = engine.boot_up()
    
    if success:
        print("\nSUCCESS: Vector Database created/updated.")
        print(f"Index saved to: {os.path.abspath('faiss_index')}")
        print("You can now run 'python app.py' to start the chat.")
    else:
        print("\nERROR: Ingestion failed. Check if 'data/' folder has PDFs.")

if __name__ == "__main__":
    try:
        run_pipeline()
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"\nCritical Error: {e}")
