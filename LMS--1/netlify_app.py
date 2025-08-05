from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# In-memory data storage for Netlify deployment
books = [
    {
        "id": 1,
        "isbn": "978-0-439-02348-1",
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "publisher": "Scholastic",
        "year": 1997,
        "genre": "Fantasy",
        "pages": 309,
        "language": "English",
        "cover_image": "https://covers.openlibrary.org/b/isbn/9780439023481-L.jpg",
        "description": "The first book in the Harry Potter series",
        "average_rating": 4.5,
        "ratings_count": 5000000,
        "stock": 10
    },
    {
        "id": 2,
        "isbn": "978-0-439-02349-8",
        "title": "Harry Potter and the Chamber of Secrets",
        "author": "J.K. Rowling",
        "publisher": "Scholastic",
        "year": 1998,
        "genre": "Fantasy",
        "pages": 341,
        "language": "English",
        "cover_image": "https://covers.openlibrary.org/b/isbn/9780439023498-L.jpg",
        "description": "The second book in the Harry Potter series",
        "average_rating": 4.6,
        "ratings_count": 4500000,
        "stock": 8
    },
    {
        "id": 3,
        "isbn": "978-0-439-02350-4",
        "title": "Harry Potter and the Prisoner of Azkaban",
        "author": "J.K. Rowling",
        "publisher": "Scholastic",
        "year": 1999,
        "genre": "Fantasy",
        "pages": 435,
        "language": "English",
        "cover_image": "https://covers.openlibrary.org/b/isbn/9780439023504-L.jpg",
        "description": "The third book in the Harry Potter series",
        "average_rating": 4.7,
        "ratings_count": 4200000,
        "stock": 12
    }
]

users = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@library.com",
        "role": "admin"
    }
]

borrow_records = []
book_ratings = []

@app.route('/')
def home():
    return jsonify({
        "message": "Library Management System API",
        "version": "1.0.0",
        "endpoints": {
            "books": "/api/books",
            "users": "/api/users",
            "borrowing": "/api/borrowing"
        }
    })

@app.route('/api/books', methods=['GET'])
def get_books():
    """Get all books with optional filtering"""
    search = request.args.get('search', '')
    genre = request.args.get('genre', '')
    
    filtered_books = books
    
    if search:
        filtered_books = [b for b in filtered_books 
                         if search.lower() in b['title'].lower() or 
                            search.lower() in b['author'].lower()]
    
    if genre:
        filtered_books = [b for b in filtered_books if b['genre'] == genre]
    
    return jsonify({
        "books": filtered_books,
        "total": len(filtered_books)
    })

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book by ID"""
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)

@app.route('/api/books/genres', methods=['GET'])
def get_genres():
    """Get all unique genres"""
    genres = list(set(b['genre'] for b in books))
    return jsonify(genres)

@app.route('/api/books/top-rated', methods=['GET'])
def get_top_rated():
    """Get top-rated books"""
    top_books = sorted(books, key=lambda x: x['average_rating'], reverse=True)[:10]
    return jsonify(top_books)

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    return jsonify(users)

@app.route('/api/borrowing', methods=['GET'])
def get_borrow_records():
    """Get all borrow records"""
    return jsonify(borrow_records)

@app.route('/api/borrowing', methods=['POST'])
def create_borrow_record():
    """Create a new borrow record"""
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'book_id' not in data:
        return jsonify({"error": "User ID and Book ID are required"}), 400
    
    book = next((b for b in books if b['id'] == data['book_id']), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    if book['stock'] <= 0:
        return jsonify({"error": "Book not available"}), 400
    
    record = {
        "id": len(borrow_records) + 1,
        "user_id": data['user_id'],
        "book_id": data['book_id'],
        "borrow_date": datetime.utcnow().isoformat(),
        "due_date": (datetime.utcnow() + timedelta(days=14)).isoformat(),
        "return_date": None,
        "status": "borrowed"
    }
    
    borrow_records.append(record)
    book['stock'] -= 1
    
    return jsonify(record), 201

@app.route('/api/books/<int:book_id>/ratings', methods=['POST'])
def add_rating(book_id):
    """Add a rating for a book"""
    data = request.get_json()
    
    if not data or 'rating' not in data:
        return jsonify({"error": "Rating is required"}), 400
    
    rating = {
        "id": len(book_ratings) + 1,
        "book_id": book_id,
        "user_id": data.get('user_id', 1),
        "rating": data['rating'],
        "review": data.get('review', ''),
        "created_at": datetime.utcnow().isoformat()
    }
    
    book_ratings.append(rating)
    
    # Update book average rating
    book_ratings_for_book = [r for r in book_ratings if r['book_id'] == book_id]
    book = next((b for b in books if b['id'] == book_id), None)
    if book:
        book['average_rating'] = sum(r['rating'] for r in book_ratings_for_book) / len(book_ratings_for_book)
        book['ratings_count'] = len(book_ratings_for_book)
    
    return jsonify({"message": "Rating added successfully"}), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
