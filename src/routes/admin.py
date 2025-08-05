from flask import Blueprint, request, jsonify
from src.app_factory import db
from src.models import User, Book, BorrowRecord, Fees
from datetime import datetime, timedelta
from sqlalchemy import func
from src.routes.auth import verify_token

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/stats', methods=['GET'])
def get_admin_stats():
    """Get admin dashboard statistics"""
    try:
        # Total users
        total_users = User.query.count()
        
        # Total books
        total_books = Book.query.count()
        
        # Total borrowed books
        total_borrowed = BorrowRecord.query.filter_by(status='borrowed').count()
        
        # Total returned books
        total_returned = BorrowRecord.query.filter_by(status='returned').count()
        
        # Total fees
        total_fees = db.session.query(func.sum(Fees.amount)).filter_by(paid=False).scalar() or 0
        
        # Recent users (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_users = User.query.filter(User.created_at >= thirty_days_ago).count()
        
        # Recent borrowings (last 30 days)
        recent_borrowings = BorrowRecord.query.filter(BorrowRecord.borrow_date >= thirty_days_ago).count()
        
        return jsonify({
            'total_users': total_users,
            'total_books': total_books,
            'total_borrowed': total_borrowed,
            'total_returned': total_returned,
            'total_outstanding_fees': float(total_fees),
            'recent_users': recent_users,
            'recent_borrowings': recent_borrowings
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/forecast', methods=['GET'])
def get_admin_forecast():
    """Get admin forecast data for future trends"""
    try:
        # Get data for the next 30 days
        today = datetime.utcnow()
        forecast_data = []
        
        # Predict borrowing trends based on historical data
        # This is a simplified forecast - in a real application, you would use ML models
        
        # Get borrowing data for the past 30 days
        thirty_days_ago = today - timedelta(days=30)
        recent_borrowings = BorrowRecord.query.filter(
            BorrowRecord.borrow_date >= thirty_days_ago
        ).all()
        
        # Calculate average daily borrowings
        daily_borrowings = {}
        for record in recent_borrowings:
            date_key = record.borrow_date.date()
            if date_key in daily_borrowings:
                daily_borrowings[date_key] += 1
            else:
                daily_borrowings[date_key] = 1
        
        avg_daily_borrowings = sum(daily_borrowings.values()) / len(daily_borrowings) if daily_borrowings else 0
        
        # Get popular genres
        genre_counts = db.session.query(
            Book.genre, func.count(BorrowRecord.id)
        ).join(Book, BorrowRecord.book_id == Book.id)\
         .filter(BorrowRecord.borrow_date >= thirty_days_ago)\
         .group_by(Book.genre)\
         .all()
        
        popular_genres = [{'genre': genre, 'count': count} for genre, count in genre_counts]
        
        # Forecast for next 7 days
        forecast = []
        for i in range(1, 8):
            future_date = today + timedelta(days=i)
            predicted_borrowings = round(avg_daily_borrowings * (1 + (i * 0.02)))  # 2% increase per day
            forecast.append({
                'date': future_date.strftime('%Y-%m-%d'),
                'predicted_borrowings': predicted_borrowings
            })
        
        return jsonify({
            'forecast': forecast,
            'popular_genres': popular_genres,
            'average_daily_borrowings': avg_daily_borrowings
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/books', methods=['GET'])
def get_all_books():
    """Get all books for admin management"""
    try:
        books = Book.query.all()
        return jsonify([{
            'id': book.id,
            'isbn': book.isbn,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'year': book.year,
            'genre': book.genre,
            'stock': book.stock,
            'average_rating': book.average_rating
        } for book in books]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/books', methods=['POST'])
def add_book():
    """Add a new book"""

@admin_bp.route('/admin/fine-calculation', methods=['GET'])
def fine_calculation():
    """Protected fine calculation page"""
    user, error_response = verify_token(request)
    if error_response:
        return error_response
    
    if user['role'] != 'admin':
        return jsonify({'error': 'Forbidden: Admin access required'}), 403
        
    return send_from_directory('public', 'fine_calculation.html')
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check required fields
        required_fields = ['title', 'author']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        new_book = Book(
            isbn=data.get('isbn'),
            title=data['title'],
            author=data['author'],
            publisher=data.get('publisher'),
            year=data.get('year'),
            genre=data.get('genre'),
            pages=data.get('pages'),
            language=data.get('language', 'English'),
            cover_image=data.get('cover_image'),
            description=data.get('description'),
            stock=data.get('stock', 1)
        )
        
        db.session.add(new_book)
        db.session.commit()
        
        return jsonify({
            'id': new_book.id,
            'message': 'Book added successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
