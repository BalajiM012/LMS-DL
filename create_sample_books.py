#!/usr/bin/env python3
"""
Script to create sample books for the Library Management System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.app_factory_minimal import create_app, db
from src.models import Book

def create_sample_books():
    """Create sample books for testing the inventory system"""
    
    sample_books = [
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'isbn': '978-0-06-112008-4',
            'category': 'Fiction',
            'total_quantity': 5,
            'available_quantity': 3,
            'description': 'A classic novel about racial injustice and childhood innocence in the American South.'
        },
        {
            'title': '1984',
            'author': 'George Orwell',
            'isbn': '978-0-452-28423-4',
            'category': 'Fiction',
            'total_quantity': 8,
            'available_quantity': 6,
            'description': 'A dystopian social science fiction novel about totalitarian control.'
        },
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'isbn': '978-0-7432-7356-5',
            'category': 'Fiction',
            'total_quantity': 4,
            'available_quantity': 2,
            'description': 'A novel about the Jazz Age and the American Dream.'
        },
        {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'isbn': '978-0-14-143951-8',
            'category': 'Fiction',
            'total_quantity': 6,
            'available_quantity': 4,
            'description': 'A romantic novel about manners, upbringing, morality, and marriage.'
        },
        {
            'title': 'The Catcher in the Rye',
            'author': 'J.D. Salinger',
            'isbn': '978-0-316-76948-0',
            'category': 'Fiction',
            'total_quantity': 3,
            'available_quantity': 1,
            'description': 'A coming-of-age story about teenage rebellion and alienation.'
        },
        {
            'title': 'A Brief History of Time',
            'author': 'Stephen Hawking',
            'isbn': '978-0-553-38016-3',
            'category': 'Science',
            'total_quantity': 7,
            'available_quantity': 5,
            'description': 'A popular science book on cosmology and theoretical physics.'
        },
        {
            'title': 'The Origin of Species',
            'author': 'Charles Darwin',
            'isbn': '978-0-14-043205-1',
            'category': 'Science',
            'total_quantity': 4,
            'available_quantity': 3,
            'description': 'The foundational work on evolutionary biology.'
        },
        {
            'title': 'Sapiens: A Brief History of Humankind',
            'author': 'Yuval Noah Harari',
            'isbn': '978-0-06-231609-7',
            'category': 'History',
            'total_quantity': 10,
            'available_quantity': 8,
            'description': 'An exploration of how Homo sapiens came to dominate Earth.'
        },
        {
            'title': 'The Art of War',
            'author': 'Sun Tzu',
            'isbn': '978-1-59030-963-7',
            'category': 'History',
            'total_quantity': 5,
            'available_quantity': 3,
            'description': 'Ancient Chinese military treatise on strategy and tactics.'
        },
        {
            'title': 'Steve Jobs',
            'author': 'Walter Isaacson',
            'isbn': '978-1-4516-4853-9',
            'category': 'Biography',
            'total_quantity': 6,
            'available_quantity': 4,
            'description': 'The authorized biography of Apple co-founder Steve Jobs.'
        },
        {
            'title': 'The Autobiography of Malcolm X',
            'author': 'Malcolm X and Alex Haley',
            'isbn': '978-0-345-35068-8',
            'category': 'Biography',
            'total_quantity': 4,
            'available_quantity': 2,
            'description': 'The life story of the influential African-American leader.'
        },
        {
            'title': 'Clean Code',
            'author': 'Robert C. Martin',
            'isbn': '978-0-13-235088-4',
            'category': 'Technology',
            'total_quantity': 8,
            'available_quantity': 6,
            'description': 'A handbook of agile software craftsmanship.'
        },
        {
            'title': 'Introduction to Algorithms',
            'author': 'Thomas H. Cormen',
            'isbn': '978-0-262-03384-8',
            'category': 'Technology',
            'total_quantity': 5,
            'available_quantity': 3,
            'description': 'Comprehensive textbook on computer algorithms.'
        },
        {
            'title': 'The Pragmatic Programmer',
            'author': 'David Thomas and Andrew Hunt',
            'isbn': '978-0-201-61622-4',
            'category': 'Technology',
            'total_quantity': 7,
            'available_quantity': 5,
            'description': 'Your journey to mastery in software development.'
        },
        {
            'title': 'Thinking, Fast and Slow',
            'author': 'Daniel Kahneman',
            'isbn': '978-0-374-53355-7',
            'category': 'Non-Fiction',
            'total_quantity': 6,
            'available_quantity': 4,
            'description': 'Insights into how the mind makes decisions.'
        },
        {
            'title': 'The Power of Habit',
            'author': 'Charles Duhigg',
            'isbn': '978-1-4000-6928-6',
            'category': 'Non-Fiction',
            'total_quantity': 5,
            'available_quantity': 3,
            'description': 'Why we do what we do in life and business.'
        },
        {
            'title': 'Educated',
            'author': 'Tara Westover',
            'isbn': '978-0-399-59050-4',
            'category': 'Biography',
            'total_quantity': 4,
            'available_quantity': 2,
            'description': 'A memoir about education, family, and the struggle for self-invention.'
        },
        {
            'title': 'The Immortal Life of Henrietta Lacks',
            'author': 'Rebecca Skloot',
            'isbn': '978-1-4000-5217-2',
            'category': 'Science',
            'total_quantity': 3,
            'available_quantity': 1,
            'description': 'The story of how one woman\'s cells changed medicine forever.'
        },
        {
            'title': 'Guns, Germs, and Steel',
            'author': 'Jared Diamond',
            'isbn': '978-0-393-31755-8',
            'category': 'History',
            'total_quantity': 5,
            'available_quantity': 3,
            'description': 'The fates of human societies and environmental factors.'
        },
        {
            'title': 'The Lean Startup',
            'author': 'Eric Ries',
            'isbn': '978-0-307-88789-4',
            'category': 'Technology',
            'total_quantity': 6,
            'available_quantity': 4,
            'description': 'How today\'s entrepreneurs use continuous innovation to create successful businesses.'
        },
        {
            'title': 'Dune',
            'author': 'Frank Herbert',
            'isbn': '978-0-441-17271-9',
            'category': 'Fiction',
            'total_quantity': 7,
            'available_quantity': 5,
            'description': 'Epic science fiction novel set in a distant future.'
        },
        {
            'title': 'The Lord of the Rings',
            'author': 'J.R.R. Tolkien',
            'isbn': '978-0-544-00341-5',
            'category': 'Fiction',
            'total_quantity': 9,
            'available_quantity': 7,
            'description': 'Epic high fantasy adventure in Middle-earth.'
        },
        {
            'title': 'Harry Potter and the Philosopher\'s Stone',
            'author': 'J.K. Rowling',
            'isbn': '978-0-439-70818-8',
            'category': 'Fiction',
            'total_quantity': 12,
            'available_quantity': 10,
            'description': 'The first book in the magical Harry Potter series.'
        },
        {
            'title': 'The Hitchhiker\'s Guide to the Galaxy',
            'author': 'Douglas Adams',
            'isbn': '978-0-345-39180-3',
            'category': 'Fiction',
            'total_quantity': 5,
            'available_quantity': 3,
            'description': 'A comedic science fiction series about space travel.'
        },
        {
            'title': 'Atomic Habits',
            'author': 'James Clear',
            'isbn': '978-0-7352-1129-2',
            'category': 'Non-Fiction',
            'total_quantity': 8,
            'available_quantity': 6,
            'description': 'An easy and proven way to build good habits and break bad ones.'
        }
    ]
    
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if books already exist
        existing_books = Book.query.count()
        if existing_books > 0:
            print(f"Database already contains {existing_books} books.")
            response = input("Do you want to add more sample books? (y/n): ")
            if response.lower() != 'y':
                print("Operation cancelled.")
                return
        
        # Add sample books
        books_added = 0
        for book_data in sample_books:
            # Check if book with this ISBN already exists
            existing_book = Book.query.filter_by(isbn=book_data['isbn']).first()
            if existing_book:
                print(f"Book with ISBN {book_data['isbn']} already exists. Skipping...")
                continue
            
            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                isbn=book_data['isbn'],
                category=book_data['category'],
                total_quantity=book_data['total_quantity'],
                available_quantity=book_data['available_quantity'],
                description=book_data['description']
            )
            
            db.session.add(book)
            books_added += 1
            print(f"Added: {book_data['title']} by {book_data['author']}")
        
        try:
            db.session.commit()
            print(f"\n✅ Successfully added {books_added} books to the inventory!")
            
            # Display summary
            total_books = Book.query.count()
            total_available = db.session.query(db.func.sum(Book.available_quantity)).scalar() or 0
            total_borrowed = db.session.query(
                db.func.sum(Book.total_quantity - Book.available_quantity)
            ).scalar() or 0
            
            print(f"\n📊 Inventory Summary:")
            print(f"   Total Books: {total_books}")
            print(f"   Available Copies: {total_available}")
            print(f"   Borrowed Copies: {total_borrowed}")
            
            # Display categories
            categories = db.session.query(Book.category).distinct().all()
            category_list = [cat[0] for cat in categories if cat[0]]
            print(f"   Categories: {', '.join(category_list)}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error adding books: {str(e)}")

if __name__ == "__main__":
    create_sample_books()
