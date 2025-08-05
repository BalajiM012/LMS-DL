#!/usr/bin/env python3
"""
Script to initialize the database with the new schema and import the book recommendation dataset
"""

from src.app_factory import create_app, db
from src.models import User, Book, BorrowRecord, Fees, BookRating, BookRecommendation
from src.utils.dataset_importer import import_book_recommendation_dataset

def init_database():
    """Initialize the database with new schema"""
    app = create_app()
    
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        print("Dropped existing tables...")
        
        # Create all new tables
        db.create_all()
        print("Created new database tables...")
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@library.com',
            password_hash='admin123',  # In production, use proper password hashing
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Created admin user...")
        
        # Import book recommendation dataset
        print("Importing book recommendation dataset...")
        count = import_book_recommendation_dataset()
        print(f"Successfully imported {count} books from the dataset")
        
        print("Database initialization complete!")

if __name__ == '__main__':
    init_database()
