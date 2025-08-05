from flask import Blueprint, request, jsonify, current_app
from flask import send_from_directory
from src.app_factory import db
from src.models import User
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
import os

auth_bp = Blueprint('auth', __name__)

def generate_token(user_id, username, role):
    """Generate JWT token for user authentication with expiration and signing"""
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow(),
        'sub': {
            'user_id': user_id,
            'username': username,
            'role': role
        }
    }
    token = jwt.encode(
        payload, 
        current_app.config['SECRET_KEY'], 
        algorithm='HS256'
    )
    return token

@auth_bp.route('/student_login/signup', methods=['POST'])
def student_signup():
    """Student signup endpoint"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Check required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if user already exists
    existing_user = User.query.filter(
        (User.username == data['username']) | (User.email == data['email'])
    ).first()
    
    if existing_user:
        return jsonify({'error': 'Username or email already exists'}), 409
    
    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role=data.get('role', 'student')  # Default to student
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    # Generate token
    token = generate_token(new_user.id, new_user.username, new_user.role)
    
    return jsonify({
        'message': 'User created successfully',
        'access_token': token,
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'role': new_user.role
        }
    }), 201

@auth_bp.route('/student_login/login', methods=['POST'])
def student_login():
    """Student login endpoint"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Check required fields
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Find user by username
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials. Please try again.'}), 401
    
    # Generate token
    token = generate_token(user.id, user.username, user.role)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

@auth_bp.route('/student_login/logout', methods=['POST'])
def student_logout():
    """Student logout endpoint"""
    # In a real implementation, you would invalidate the token
    # For now, we'll just return a success message
    return jsonify({'message': 'Logout successful'}), 200

# Token verification middleware
def verify_token(request):
    """Verify JWT token and return user info if valid"""
    token = request.headers.get('Authorization')
    
    if not token:
        return None, jsonify({'error': 'Missing token'}), 401
    
    try:
        # Remove 'Bearer ' prefix if present
        token = token.replace('Bearer ', '', 1)
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['sub'], None
    except jwt.ExpiredSignatureError:
        return None, jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return None, jsonify({'error': 'Invalid token'}), 401

@auth_bp.route('/student')
def student_page():
    """Protected student dashboard page"""
    user, error_response = verify_token(request)
    if error_response:
        return error_response
    
    if user['role'] != 'student':
        return jsonify({'error': 'Forbidden: Student access required'}), 403
        
    return send_from_directory('public', 'student.html')

@auth_bp.route('/admin')
def admin_page():
    """Protected admin dashboard page"""
    user, error_response = verify_token(request)
    if error_response:
        return error_response
    
    if user['role'] != 'admin':
        return jsonify({'error': 'Forbidden: Admin access required'}), 403
        
    return send_from_directory('public', 'admin.html')
