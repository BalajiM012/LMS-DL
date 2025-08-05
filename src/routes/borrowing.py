from flask import Blueprint, request, jsonify
from src.app_factory import db
from src.models import BorrowRecord, Book, User
from datetime import datetime, timedelta

borrowing_bp = Blueprint('borrowing', __name__)

@borrowing_bp.route('/', methods=['GET'])
def get_borrow_records():
    """Get all borrow records"""
    records = BorrowRecord.query.all()
    return jsonify([{
        'id': record.id,
        'user': {
            'id': record.user.id,
            'username': record.user.username
        },
        'book': {
            'id': record.book.id,
            'title': record.book.title,
            'author': record.book.author
        },
        'borrow_date': record.borrow_date.isoformat(),
        'due_date': record.due_date.isoformat(),
        'return_date': record.return_date.isoformat() if record.return_date else None,
        'status': record.status
    } for record in records])

@borrowing_bp.route('/', methods=['POST'])
def create_borrow_record():
    """Create a new borrow record"""
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'book_id' not in data:
        return jsonify({'error': 'User ID and Book ID are required'}), 400
    
    book = Book.query.get(data['book_id'])
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    if book.stock <= 0:
        return jsonify({'error': 'Book not available'}), 400
    
    borrow_record = BorrowRecord(
        user_id=data['user_id'],
        book_id=data['book_id'],
        due_date=datetime.utcnow() + timedelta(days=14)
    )
    
    book.stock -= 1
    
    db.session.add(borrow_record)
    db.session.commit()
    
    return jsonify({
        'id': borrow_record.id,
        'user_id': borrow_record.user_id,
        'book_id': borrow_record.book_id,
        'due_date': borrow_record.due_date.isoformat(),
        'status': borrow_record.status
    }), 201

@borrowing_bp.route('/<int:record_id>/return', methods=['PUT'])
def return_book(record_id):
    """Return a borrowed book"""
    record = BorrowRecord.query.get_or_404(record_id)
    
    if record.status == 'returned':
        return jsonify({'error': 'Book already returned'}), 400
    
    record.return_date = datetime.utcnow()
    record.status = 'returned'
    
    book = Book.query.get(record.book_id)
    book.stock += 1
    
    db.session.commit()
    
    return jsonify({
        'id': record.id,
        'return_date': record.return_date.isoformat(),
        'status': record.status
    })
