"""
Test script for TensorFlow integration in Library Management System
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_tensorflow_status():
    """Test TensorFlow status endpoint"""
    print("Testing TensorFlow status...")
    try:
        response = requests.get(f"{BASE_URL}/api/tensorflow/status")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_book_recommendations():
    """Test book recommendations endpoint"""
    print("\nTesting book recommendations...")
    try:
        # First login to create a session
        login_data = {
            "username": "student1",
            "password": "password123"
        }
        
        # Since we can't actually login in this test, we'll test the endpoint directly
        response = requests.get(f"{BASE_URL}/api/tensorflow/recommendations")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_demand_forecast():
    """Test demand forecast endpoint"""
    print("\nTesting demand forecast...")
    try:
        response = requests.get(f"{BASE_URL}/api/tensorflow/demand_forecast")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_fine_prediction():
    """Test fine prediction endpoint"""
    print("\nTesting fine prediction...")
    try:
        data = {
            "student_id": 1,
            "book_id": 1
        }
        response = requests.post(f"{BASE_URL}/api/tensorflow/fine_prediction", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_due_date_tracking():
    """Test due date tracking endpoint"""
    print("\nTesting due date tracking...")
    try:
        # Since we can't create a session in this test, we'll test the endpoint directly
        response = requests.get(f"{BASE_URL}/api/tensorflow/due_date_tracking")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_book_demand(book_id=1):
    """Test book demand endpoint"""
    print(f"\nTesting book demand for book_id: {book_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/tensorflow/book_demand/{book_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Main test function"""
    print("Testing TensorFlow Integration Endpoints")
    print("=" * 50)
    
    # Test all endpoints
    test_tensorflow_status()
    test_book_recommendations()
    test_demand_forecast()
    test_fine_prediction()
    test_due_date_tracking()
    test_book_demand()
    
    print("\n" + "=" * 50)
    print("TensorFlow Integration Tests Completed")

if __name__ == "__main__":
    main()
