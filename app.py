import os
from flask import Flask
from src.api.routes import main_bp
from src.core.engine import MedicalEngine
from flask_apscheduler import APScheduler

class Config:
    SCHEDULER_API_ENABLED = True

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    
    # Initialize Engine
    engine = MedicalEngine()
    
    # Initialize Scheduler
    scheduler = APScheduler()
    
    # Define the background task
    @scheduler.task('interval', id='sync_docs', seconds=60) # Scans every 60 seconds
    def scheduled_sync():
        with app.app_context():
            print("🔍 Periodic scan: Checking for new clinical documents...")
            engine.sync_new_data()

    scheduler.init_app(app)
    scheduler.start()

    # Passing the engine to the blueprint so routes can access it
    app.engine = engine 
    app.register_blueprint(main_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)