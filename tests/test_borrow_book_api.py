import pytest
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app_factory import create_app, db
from src.models import Book, User, BorrowRecord
from datetime import datetime, timedelta

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create sample user and book
            user = User(fullname='Borrow Test User', email='borrowtest@example.com', username='borrowtestuser', password='testpass')
            db.session.add(user)
            db.session.commit()
            book = Book(title='Borrow Test Book', author='Author B', isbn='9876543210', copies=2)
            db.session.add(book)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_borrow_book_success(client):
    with client.application.app_context():
        # Ensure no borrow records exist initially
        BorrowRecord.query.delete()
        db.session.commit()

    response = client.post('/api/student/borrow_book', json={'book_id': 1, 'user_id': 1})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'message' in data
    assert 'borrowed successfully' in data['message']

def test_borrow_book_missing_params(client):
    response = client.post('/api/student/borrow_book', json={})
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'error' in data

def test_borrow_book_invalid_book(client):
    response = client.post('/api/student/borrow_book', json={'book_id': 999, 'user_id': 1})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert 'error' in data

def test_borrow_book_no_copies(client):
    # Borrow all copies first
    client.post('/api/student/borrow_book', json={'book_id': 1, 'user_id': 1})
    client.post('/api/student/borrow_book', json={'book_id': 1, 'user_id': 1})
    # Now no copies left
    response = client.post('/api/student/borrow_book', json={'book_id': 1, 'user_id': 1})
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'error' in data
