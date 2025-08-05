import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/book_management"

def test_get_books():
    url = f"{BASE_URL}/books"
    response = requests.get(url)
    print("Get books response status:", response.status_code)
    print("Get books response text:", response.text)
    assert response.status_code == 200
    try:
        data = response.json()
    except Exception as e:
        pytest.fail(f"Response is not valid JSON: {e}")
    assert isinstance(data, list)

def test_add_book():
    url = f"{BASE_URL}/books"
    payload = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "1234567890",
        "copies": 5
    }
    response = requests.post(url, json=payload)
    print("Add book response status:", response.status_code)
    print("Add book response text:", response.text)
    assert response.status_code == 200
    data = response.json()
    assert data.get("message") == "Book added"
