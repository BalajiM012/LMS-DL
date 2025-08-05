import requests
import json

# Test admin login
def test_admin_login():
    url = "http://localhost:5000/api/admin_login/login"
    payload = {
        "username": "newadmin",
        "password": "newadminpassword"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response
    except Exception as e:
        print(f"Error: {e}")

# Test demand forecast
def test_demand_forecast():
    url = "http://localhost:5000/demand_forecast/forecast"
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing admin login...")
    test_admin_login()
    print("\nTesting demand forecast...")
    test_demand_forecast()
