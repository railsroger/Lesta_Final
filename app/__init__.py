from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    
    db.init_app(app)
    
    # Ждем пока PostgreSQL будет готов
    with app.app_context():
        max_retries = 5
        for _ in range(max_retries):
            try:
                db.create_all()
                break
            except:
                time.sleep(2)
    
    from .routes import main
    app.register_blueprint(main)
    
    return app
