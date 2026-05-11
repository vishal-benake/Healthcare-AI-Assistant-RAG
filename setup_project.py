import os
from pathlib import Path

def setup_current_directory():
    # Set the root to the current working directory where the script is located
    root = Path.cwd()

    # Define the directory structure
    directories = [
        "src/api",
        "src/core",
        "src/data_handlers",
        "src/utils",
        "templates",
        "static/css",
    ]

    # Content for setup.py using your specific logic
    setup_py_content = """from setuptools import find_packages, setup
        from typing import List

        HYPEN_E_DOT = '-e .'

        def get_requirements(file_path: str) -> List[str]:
            '''
            this function will return the list of requirements
            '''
            requirements = []
            with open(file_path) as file_obj:
                requirements = file_obj.readlines()
                requirements = [req.replace("\\n", "") for req in requirements]

                if HYPEN_E_DOT in requirements:
                    requirements.remove(HYPEN_E_DOT)
            
            return requirements

        setup(
            name='Customer-Churn-Prediction-ML-Flask',
            version='0.0.1',
            author='Vishal',
            author_email='benakevishal2017@gmail.com',
            packages=find_packages(),
            install_requires=get_requirements('requirements.txt')
        )
        """

    # Define files to create with boilerplate
    files = {
        ".env": "GROQ_API_KEY=your_key_here\nEMBEDDING_MODEL=all-MiniLM-L6-v2",
        "requirements.txt": (
            "flask\n"
            "groq\n"
            "python-dotenv\n"
            "pandas\n"
            "sentence-transformers\n"
            "chromadb\n"
            "lxml\n"
            "-e ."
        ),
        "src/__init__.py": "",
        "app.py": (
            "from flask import Flask, render_template\n"
            "from src.api.routes import api_bp\n\n"
            "app = Flask(__name__)\n"
            "app.register_blueprint(api_bp)\n\n"
            "@app.route('/')\n"
            "def index():\n"
            "    return render_template('index.html')\n\n"
            "if __name__ == '__main__':\n"
            "    app.run(debug=True, port=5000)"
        ),
        "setup.py": setup_py_content,
        "src/api/__init__.py": "",
        "src/api/routes.py": (
            "from flask import Blueprint, jsonify, request\n\n"
            "api_bp = Blueprint('api', __name__, url_prefix='/api')\n\n"
            "@api_bp.route('/query', methods=['POST'])\n"
            "def handle_query():\n"
            "    return jsonify({'status': 'ready'})"
        ),
        "src/core/__init__.py": "",
        "src/core/engine.py": "class RAGEngine:\n    def __init__(self):\n        pass",
        "src/core/embedder.py": "class Embedder:\n    def __init__(self):\n        pass",
        "src/core/llm_handler.py": "class LLMHandler:\n    def __init__(self):\n        pass",
        "src/data_handlers/__init__.py": "",
        "src/data_handlers/xml_parser.py": "def parse_xml(file_path):\n    pass",
        "src/data_handlers/csv_handler.py": "def handle_csv(file_path):\n    pass",
        "src/data_handlers/ingestor.py": "def walk_directory(path):\n    pass",
        "src/utils/__init__.py": "",
        "src/utils/logger.py": "import logging\n\nlogging.basicConfig(level=logging.INFO)",
        "src/utils/config.py": "import os\nfrom dotenv import load_dotenv\n\nload_dotenv()",
        "templates/index.html": (
            "<!DOCTYPE html>\n<html>\n<head>\n"
            "    <link rel='stylesheet' href='/static/css/style.css'>\n"
            "    <title>RAG System</title>\n"
            "</head>\n<body>\n    <h1>RAG Explorer</h1>\n</body>\n</html>"
        ),
        "static/css/style.css": "body { font-family: Arial; background: #f4f4f4; padding: 20px; }",
    }

    print(f"Creating project structure in: {root}")

    # Create the directories
    for folder in directories:
        folder_path = root / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        # Create __init__.py automatically for packages
        (folder_path / "__init__.py").touch()

    # Create the files
    for file_path, content in files.items():
        full_path = root / file_path
        
        # Ensure parent folder exists (mostly for files in root)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file if it doesn't already exist
        if not full_path.exists():
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Created: {file_path}")
        else:
            print(f"Skipped: {file_path} (Already exists)")

    print("\nDone! Your modular RAG structure is ready.")

if __name__ == "__main__":
    setup_current_directory()