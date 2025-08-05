#!/usr/bin/env python3
"""
Script to create test users for the Library Management System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.app_factory_minimal import create_app, db
from src.models import User
from werkzeug.security import generate_password_hash

def create_test_users():
    """Create test users for authentication testing"""
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if test users already exist
        existing_student = User.query.filter_by(username='student').first()
        existing_admin = User.query.filter_by(username='admin').first()
        
        if not existing_student:
            # Create test student user
            student_user = User(
                fullname='Test Student',
                email='student@test.com',
                username='student',
                password=generate_password_hash('student123'),
                role='student'
            )
            db.session.add(student_user)
            print("✅ Created test student user:")
            print("   Username: student")
            print("   Password: student123")
            print("   Email: student@test.com")
        else:
            print("ℹ️  Test student user already exists")
        
        if not existing_admin:
            # Create test admin user
            admin_user = User(
                fullname='Test Admin',
                email='admin@test.com',
                username='admin',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin_user)
            print("✅ Created test admin user:")
            print("   Username: admin")
            print("   Password: admin123")
            print("   Email: admin@test.com")
        else:
            print("ℹ️  Test admin user already exists")
        
        try:
            db.session.commit()
            print("\n🎉 Test users created successfully!")
            print("\nYou can now test the authentication system with:")
            print("Student Login: username='student', password='student123'")
            print("Admin Login: username='admin', password='admin123'")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating test users: {e}")

if __name__ == '__main__':
    create_test_users()
