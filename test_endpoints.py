import requests
import json

# Test student login
def test_student_login():
    url = "http://localhost:5000/api/student_login/login"
    payload = {
        "username": "newstudent",
        "password": "newstudentpassword"
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

if __name__ == "__main__":
    test_student_login()
