#!/usr/bin/env python3
"""
Test script to verify dataset integration
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_api_endpoints():
    """Test all API endpoints"""
    
    print("Testing Library Management System with Dataset Integration...")
    print("=" * 60)
    
    # Test 1: Get all books
    print("\n1. Testing GET /api/books")
    try:
        response = requests.get(f"{BASE_URL}/api/books")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: Found {len(data['books'])} books")
            if data['books']:
                print(f"   Sample book: {data['books'][0]['title']}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Get genres
    print("\n2. Testing GET /api/books/genres")
    try:
        response = requests.get(f"{BASE_URL}/api/books/genres")
        if response.status_code == 200:
            genres = response.json()
            print(f"✅ Success: Found {len(genres)} genres")
            print(f"   Genres: {', '.join(genres)}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Get top-rated books
    print("\n3. Testing GET /api/books/top-rated")
    try:
        response = requests.get(f"{BASE_URL}/api/books/top-rated")
        if response.status_code == 200:
            books = response.json()
            print(f"✅ Success: Found {len(books)} top-rated books")
            if books:
                print(f"   Top book: {books[0]['title']} (Rating: {books[0]['average_rating']})")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Search books
    print("\n4. Testing GET /api/books?search=harry")
    try:
        response = requests.get(f"{BASE_URL}/api/books?search=harry")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: Found {len(data['books'])} books matching 'harry'")
            for book in data['books'][:3]:
                print(f"   - {book['title']} by {book['author']}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Get book recommendations
    print("\n5. Testing GET /api/books/1/recommendations")
    try:
        response = requests.get(f"{BASE_URL}/api/books/1/recommendations")
        if response.status_code == 200:
            recommendations = response.json()
            print(f"✅ Success: Found {len(recommendations)} recommendations")
            for rec in recommendations[:3]:
                print(f"   - {rec['book']['title']} (Score: {rec['score']})")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Get users
    print("\n6. Testing GET /api/users")
    try:
        response = requests.get(f"{BASE_URL}/api/users")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Success: Found {len(users)} users")
            for user in users:
                print(f"   - {user['username']} ({user['email']})")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_server_tests():
    """Run comprehensive server tests"""
    print("\n" + "=" * 60)
    print("RUNNING COMPREHENSIVE TESTS...")
    print("=" * 60)
    
    # Import and run tests
    try:
        from src.app_factory import create_app, db
        from src.models import Book
        
        app = create_app()
        with app.app_context():
            # Test database connection
            print("\n1. Testing database connection...")
            try:
                book_count = Book.query.count()
                print(f"✅ Database connected successfully")
                print(f"   Total books in database: {book_count}")
            except Exception as e:
                print(f"❌ Database connection failed: {e}")
            
            # Test model relationships
            print("\n2. Testing model relationships...")
            try:
                book = Book.query.first()
                if book:
                    print(f"✅ Book model working: {book.title}")
                    print(f"   ISBN: {book.isbn}")
                    print(f"   Author: {book.author}")
                    print(f"   Genre: {book.genre}")
                    print(f"   Stock: {book.stock}")
                else:
                    print("⚠️ No books found in database")
            except Exception as e:
                print(f"❌ Model test failed: {e}")
                
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")

if __name__ == '__main__':
    print("Library Management System - Dataset Integration Test")
    print("Make sure the server is running: python app.py")
    print("Then run this test script in another terminal")
    
    choice = input("\nRun tests? (1=API tests, 2=Database tests, 3=Both): ").strip()
    
    if choice == '1':
        test_api_endpoints()
    elif choice == '2':
        run_server_tests()
    elif choice == '3':
        test_api_endpoints()
        run_server_tests()
    else:
        print("Invalid choice. Exiting.")
