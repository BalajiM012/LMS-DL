from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../library_db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from src.routes.books import books_bp
    from src.routes.users import users_bp
    from src.routes.borrowing import borrowing_bp
    from src.routes.auth import auth_bp
    from src.routes.admin import admin_bp
    
    app.register_blueprint(books_bp, url_prefix='/api/books')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(borrowing_bp, url_prefix='/api/borrowing')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    
    return app
