import pytest
import requests

def test_login():
    url = "http://127.0.0.1:5000/user/login"
    payload = {"username": "admin", "password": "password"}
    response = requests.post(url, json=payload)
    print("Login response status:", response.status_code)
    print("Login response text:", response.text)
    assert response.status_code == 200
    try:
        data = response.json()
    except Exception as e:
        pytest.fail(f"Response is not valid JSON: {e}")
    assert data.get("message") == "Login successful"

def test_history():
    # Placeholder for history test
    assert True
