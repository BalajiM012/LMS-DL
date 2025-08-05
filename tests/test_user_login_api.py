import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app_factory import create_app, db
from src.models import User
from werkzeug.security import generate_password_hash
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        # Insert test user
        if not User.query.filter_by(username='admin').first():
            user = User(
                fullname='Admin User',
                email='admin@example.com',
                username='admin',
                password=generate_password_hash('password'),
                role='admin'
            )
            db.session.add(user)
            db.session.commit()
    with app.test_client() as client:
        yield client

def test_login_success(client):
    response = client.post('/user/login', json={'username': 'admin', 'password': 'password'})
    print("Login response status:", response.status_code)
    print("Login response data:", response.data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Login successful'
    assert data['user']['username'] == 'admin'

def test_login_failure(client):
    response = client.post('/user/login', json={'username': 'admin', 'password': 'wrongpass'})
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
