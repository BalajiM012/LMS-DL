from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET', 'your-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:postgres@localhost:5432/library_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # Initialize extensions
    db.init_app(app)
    Session(app)
    
    # Register blueprints
    from src.routes.auth import auth_bp
    from src.routes.books import books_bp
    from src.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(books_bp, url_prefix='/api/books')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    return app
