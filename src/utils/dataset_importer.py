import pandas as pd
import requests
from src.app_factory import db
from src.models import Book, BookRating, BookRecommendation
from datetime import datetime
import json
import os
from flask import current_app
from docx import Document as DocxDocument
from openpyxl import Workbook

def import_book_recommendation_dataset():
    """
    Import books from the book recommendation dataset
    Dataset URL: https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset
    """
    try:
        # For demonstration, we'll create sample data similar to the dataset
        # In production, you would download and process the actual dataset
        
        sample_books = [
            {
                'isbn': '978-0-439-02348-1',
                'title': 'Harry Potter and the Sorcerer\'s Stone',
                'author': 'J.K. Rowling',
                'publisher': 'Scholastic',
                'year': 1997,
                'genre': 'Fantasy',
                'pages': 309,
                'language': 'English',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780439023481-L.jpg',
                'description': 'The first book in the Harry Potter series',
                'average_rating': 4.5,
                'ratings_count': 5000000,
                'stock': 10
            },
            {
                'isbn': '978-0-439-02349-8',
                'title': 'Harry Potter and the Chamber of Secrets',
                'author': 'J.K. Rowling',
                'publisher': 'Scholastic',
                'year': 1998,
                'genre': 'Fantasy',
                'pages': 341,
                'language': 'English',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780439023498-L.jpg',
                'description': 'The second book in the Harry Potter series',
                'average_rating': 4.6,
                'ratings_count': 4500000,
                'stock': 8
            },
            {
                'isbn': '978-0-439-02350-4',
                'title': 'Harry Potter and the Prisoner of Azkaban',
                'author': 'J.K. Rowling',
                'publisher': 'Scholastic',
                'year': 1999,
                'genre': 'Fantasy',
                'pages': 435,
                'language': 'English',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780439023504-L.jpg',
                'description': 'The third book in the Harry Potter series',
                'average_rating': 4.7,
                'ratings_count': 4200000,
                'stock': 12
            },
            {
                'isbn': '978-0-439-02351-1',
                'title': 'Harry Potter and the Goblet of Fire',
                'author': 'J.K. Rowling',
                'publisher': 'Scholastic',
                'year': 2000,
                'genre': 'Fantasy',
                'pages': 734,
                'language': 'English',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780439023511-L.jpg',
                'description': 'The fourth book in the Harry Potter series',
                'average_rating': 4.8,
                'ratings_count': 4000000,
                'stock': 15
            },
            {
                'isbn': '978-0-439-02352-8',
                'title': 'Harry Potter and the Order of the Phoenix',
                'author': 'J.K. Rowling',
                'publisher': 'Scholastic',
                'year': 2003,
                'genre': 'Fantasy',
                'pages': 870,
                'language': 'English',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780439023528-L.jpg',
                'description': 'The fifth book in the Harry Potter series',
                'average_rating': 4.6,
                'ratings_count': 3800000,
                'stock': 7
            },
            {
                'isbn': '978-0-439-02353-5',
                'title': 'Harry Potter and the Half-Blood Prince',
                'author': 'J.K. Rowling',
                'publisher': 'Scholastic',
                'year': 2005,
                'genre': 'Fantasy',
                'pages': 652,
                'language': 'English',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780439023535-L.jpg',
                'description': 'The sixth book in the Harry Potter series',
                'average_rating': 4.7,
                'ratings_count': 3600000,
                'stock': 9
            },
            {
                'isbn': '978-0-439-02354-2',
                'title': 'Harry Potter and the Deathly Hallows',
                'author': 'J.K. Rowling',
                'publisher': 'Scholastic',
                'year': 2007,
                'genre': 'Fantasy',
                'pages': 759,
                'language': 'English',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780439023542-L.jpg',
                'description': 'The seventh book in the Harry Potter series',
                'average_rating': 4.9,
                'ratings_count': 3500000,
                'stock': 11
            },
            {
                'isbn': '978-0-439-02355-9',
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'publisher': 'Houghton Mifflin',
                'year': 1937,
                'genre': 'Fantasy',
                'pages': 310,
                'language': 'English',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780439023559-L.jpg',
                'description': 'A fantasy novel and children\'s book by English author J. R. R. Tolkien',
                'average_rating': 4.3,
                'ratings_count': 3000000,
                'stock': 20
            },
            {
                'isbn': '978-0-439-02356-6',
                'title': 'The Lord of the Rings',
                'author': 'J.R.R. Tolkien',
                'publisher': 'Houghton Mifflin',
                'year': 1954,
                'genre': 'Fantasy',
                'pages': 1216,
                'language': 'English',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780439023566-L.jpg',
                'description': 'An epic high-fantasy novel by English author and scholar J. R. R. Tolkien',
                'average_rating': 4.6,
                'ratings_count': 2500000,
                'stock': 5
            },
            {
                'isbn': '978-0-439-02357-3',
                'title': 'The Chronicles of Narnia',
                'author': 'C.S. Lewis',
                'publisher': 'HarperCollins',
                'year': 1950,
                'genre': 'Fantasy',
                'pages': 767,
                'language': 'English',
                'cover_image': 'https://covers.openlibrary.org/b/isbn/9780439023573-L.jpg',
                'description': 'A series of seven high fantasy novels by C. S. Lewis',
                'average_rating': 4.2,
                'ratings_count': 2000000,
                'stock': 15
            }
        ]
        
    # Import books
    imported_count = 0
    for book_data in sample_books:
            existing_book = Book.query.filter_by(isbn=book_data['isbn']).first()
            if not existing_book:
                new_book = Book(**book_data)
                db.session.add(new_book)
                imported_count += 1
        
        db.session.commit()
        
        # Create sample recommendations
        recommendations = [
            {'book_id': 1, 'recommended_book_id': 2, 'score': 0.95},
            {'book_id': 1, 'recommended_book_id': 3, 'score': 0.90},
            {'book_id': 2, 'recommended_book_id': 1, 'score': 0.92},
            {'book_id': 2, 'recommended_book_id': 3, 'score': 0.88},
            {'book_id': 3, 'recommended_book_id': 1, 'score': 0.89},
            {'book_id': 3, 'recommended_book_id': 2, 'score': 0.91},
            {'book_id': 8, 'recommended_book_id': 9, 'score': 0.85},
            {'book_id': 9, 'recommended_book_id': 8, 'score': 0.87},
            {'book_id': 9, 'recommended_book_id': 10, 'score': 0.83},
            {'book_id': 10, 'recommended_book_id': 9, 'score': 0.82}
        ]
        
        for rec_data in recommendations:
            existing_rec = BookRecommendation.query.filter_by(
                book_id=rec_data['book_id'],
                recommended_book_id=rec_data['recommended_book_id']
            ).first()
            
            if not existing_rec:
                new_rec = BookRecommendation(**rec_data)
                db.session.add(new_rec)
        
        db.session.commit()
        
        return imported_count
        
    except Exception as e:
        db.session.rollback()
        raise e

def import_goodreads_dataset():
    """
    Import books from the Goodreads dataset
    Dataset URL: https://www.kaggle.com/datasets/bahramjannesarr/goodreads-book-datasets-10m
    """
    try:
        # For CSV import
        if not os.path.exists(current_app.config['GOODREADS_CSV_PATH']):
            return 0
            
        df = pd.read_csv(current_app.config['GOODREADS_CSV_PATH'])
        imported_count = 0
        
        for _, row in df.iterrows():
            book_data = {
                'isbn': str(row['isbn']),
                'title': row['title'],
                'author': row['author'],
                'publisher': row.get('publisher', ''),
                'year': row.get('year', 0),
                'genre': row.get('genre', ''),
                'pages': row.get('pages', 0),
                'language': row.get('language', ''),
                'cover_image': row.get('cover_image', ''),
                'description': row.get('description', ''),
                'average_rating': row.get('average_rating', 0.0),
                'ratings_count': row.get('ratings_count', 0),
                'stock': row.get('stock', 0)
            }
            
            existing_book = Book.query.filter_by(isbn=book_data['isbn']).first()
            if not existing_book:
                new_book = Book(**book_data)
                db.session.add(new_book)
                imported_count += 1
                
        db.session.commit()
        return imported_count
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Goodreads dataset import error: {str(e)}")
        raise e
    # For now, returning a placeholder
    return 0

def export_books_to_csv():
    """Export all books to CSV format"""
    try:
        books = Book.query.all()
        df = pd.DataFrame([{
            'isbn': book.isbn,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'year': book.year,
            'genre': book.genre,
            'pages': book.pages,
            'language': book.language,
            'cover_image': book.cover_image,
            'description': book.description,
            'average_rating': book.average_rating,
            'ratings_count': book.ratings_count,
            'stock': book.stock
        } for book in books])
        
        export_path = current_app.config['BOOKS_EXPORT_CSV']
        df.to_csv(export_path, index=False)
        return export_path
        
    except Exception as e:
        current_app.logger.error(f"CSV export error: {str(e)}")
        raise e

def export_books_to_excel():
    """Export all books to Excel format"""
    try:
        books = Book.query.all()
        wb = Workbook()
        ws = wb.active
        
        # Add headers
        ws.append([
            'ISBN', 'Title', 'Author', 'Publisher', 'Year', 'Genre', 
            'Pages', 'Language', 'Cover Image', 'Description', 'Average Rating',
            'Ratings Count', 'Stock'
        ])
        
        # Add data
        for book in books:
            ws.append([
                book.isbn, book.title, book.author, book.publisher, book.year,
                book.genre, book.pages, book.language, book.cover_image,
                book.description, book.average_rating, book.ratings_count,
                book.stock
            ])
            
        export_path = current_app.config['BOOKS_EXPORT_EXCEL']
        wb.save(export_path)
        return export_path
        
    except Exception as e:
        current_app.logger.error(f"Excel export error: {str(e)}")
        raise e

def import_books_from_word():
    """Import books from Word document"""
    try:
        if not os.path.exists(current_app.config['BOOKS_IMPORT_WORD']):
            return 0
            
        doc = DocxDocument(current_app.config['BOOKS_IMPORT_WORD'])
        table = doc.tables[0]
        
        imported_count = 0
        for row in table.rows[1:]:  # Skip header row
            cells = row.cells
            if len(cells) < 13:  # Ensure minimum required columns
                continue
                
            book_data = {
                'isbn': cells[0].text.strip(),
                'title': cells[1].text.strip(),
                'author': cells[2].text.strip(),
                'publisher': cells[3].text.strip(),
                'year': int(cells[4].text.strip()) if cells[4].text.strip().isdigit() else 0,
                'genre': cells[5].text.strip(),
                'pages': int(cells[6].text.strip()) if cells[6].text.strip().isdigit() else 0,
                'language': cells[7].text.strip(),
                'cover_image': cells[8].text.strip(),
                'description': cells[9].text.strip(),
                'average_rating': float(cells[10].text.strip()) if cells[10].text.strip().replace('.', '', 1).isdigit() else 0.0,
                'ratings_count': int(cells[11].text.strip()) if cells[11].text.strip().isdigit() else 0,
                'stock': int(cells[12].text.strip()) if cells[12].text.strip().isdigit() else 0
            }
            
            existing_book = Book.query.filter_by(isbn=book_data['isbn']).first()
            if not existing_book:
                new_book = Book(**book_data)
                db.session.add(new_book)
                imported_count += 1
                
        db.session.commit()
        return imported_count
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Word import error: {str(e)}")
        raise e

def import_library_books_dataset():
    """
    Import books from the library books dataset
    Dataset URL: https://www.kaggle.com/datasets/bimalgajera/library-books
    """
    try:
        # For Excel import
        if not os.path.exists(current_app.config['LIBRARY_EXCEL_PATH']):
            return 0
            
        df = pd.read_excel(current_app.config['LIBRARY_EXCEL_PATH'])
        imported_count = 0
        
        for _, row in df.iterrows():
            book_data = {
                'isbn': str(row['ISBN']),
                'title': row['Title'],
                'author': row['Author'],
                'publisher': row.get('Publisher', ''),
                'year': row.get('Year', 0),
                'genre': row.get('Genre', ''),
                'pages': row.get('Pages', 0),
                'language': row.get('Language', ''),
                'cover_image': row.get('CoverImage', ''),
                'description': row.get('Description', ''),
                'average_rating': row.get('Rating', 0.0),
                'ratings_count': row.get('RatingsCount', 0),
                'stock': row.get('Stock', 0)
            }
            
            existing_book = Book.query.filter_by(isbn=book_data['isbn']).first()
            if not existing_book:
                new_book = Book(**book_data)
                db.session.add(new_book)
                imported_count += 1
                
        db.session.commit()
        return imported_count
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Library books dataset import error: {str(e)}")
        raise e
    # For now, returning a placeholder
    return 0

def import_sf_library_usage_dataset():
    """
    Import library usage data from the SF library dataset
    Dataset URL: https://www.kaggle.com/datasets/datasf/sf-library-usage-data
    """
    try:
        # For TXT import
        if not os.path.exists(current_app.config['USAGE_TXT_PATH']):
            return 0
            
        with open(current_app.config['USAGE_TXT_PATH'], 'r') as f:
            lines = f.readlines()
            
        # Process and save usage data
        return len(lines)
        
    except Exception as e:
        current_app.logger.error(f"SF library usage import error: {str(e)}")
        raise e
    # For now, returning a placeholder
    return 0
