from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import time

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:postgres@db:5432/attendance'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    db.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
    with app.app_context():
        # Reintentar conexión a la base de datos
        max_retries = 5
        for attempt in range(max_retries):
            try:
                db.create_all()
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"DB connection attempt {attempt + 1} failed, retrying in 5s...")
                    time.sleep(5)
                else:
                    raise e
    
    return app
