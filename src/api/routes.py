from flask import Blueprint, render_template, request, jsonify
from src.core.engine import MedicalEngine

main_bp = Blueprint('main', __name__)
# Initialize the engine once so it persists
engine = MedicalEngine()

@main_bp.route('/')
def home():
    
    return render_template('index.html')

@main_bp.route('/ask', methods=['POST'])
def ask():
    try:
        user_msg = request.json.get("message")
        if not user_msg:
            return jsonify({"answer": "Empty query received."}), 400
            
        result = engine.query(user_msg)
        return jsonify(result)
    except Exception as e:
        return jsonify({"answer": f"API Error: {str(e)}"}), 500

@main_bp.route('/ingest', methods=['POST'])
def ingest():
    success = engine.boot_up()
    return jsonify({"success": success})