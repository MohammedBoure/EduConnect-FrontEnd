import requests
import json

# Base URL for the Flask server (adjust to your server's address)
BASE_URL = "https://educonnect-wp9t.onrender.com/api"

def test_register():
    """
    Test the /register API endpoint with various scenarios:
    - Valid registration
    - Duplicate email
    - Missing required fields
    - Short password
    """
    print("Testing Register API...")
    
    # Test case 1: Valid registration
    valid_user = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "department": "Computer Science",
        "skills": ["Python", "JavaScript"],
        "photo": "profile.jpg"
    }
    
    for i in  ["name1","name2", "name3","name4","name5"]:
        valid_user["first_name"] = "value"
        valid_user["email"] = f"{i}@gmail.com"
        response = requests.post(f"{BASE_URL}/register", json=valid_user)
        print(f"Valid registration response: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    
    # Test case 2: Duplicate email
    response = requests.post(f"{BASE_URL}/register", json=valid_user)
    print(f"\nDuplicate email response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Test case 3: Missing required fields
    invalid_user = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=invalid_user)
    print(f"\nMissing fields response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Test case 4: Short password
    short_password_user = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "password": "short",
        "department": "Computer Science",
        "skills": ["Python"]
    }
    
    response = requests.post(f"{BASE_URL}/register", json=short_password_user)
    print(f"\nShort password response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_login():
    """
    Test the /login API endpoint with various scenarios:
    - Valid login
    - Wrong password
    - Non-existent email
    - Missing credentials
    """
    print("\nTesting Login API...")
    
    # Register a user for login testing
    user = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test.user@example.com",
        "password": "testpassword123",
        "department": "Computer Science",
        "skills": ["Python"],
        "photo": "test.jpg"
    }
    
    requests.post(f"{BASE_URL}/register", json=user)
    
    # Test case 1: Valid login
    login_data = {
        "email": "test.user@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Valid login response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Test case 2: Wrong password
    wrong_password = {
        "email": "test.user@example.com",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=wrong_password)
    print(f"\nWrong password response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Test case 3: Non-existent email
    wrong_email = {
        "email": "nonexistent@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=wrong_email)
    print(f"\nNon-existent email response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Test case 4: Missing credentials
    incomplete_data = {
        "email": "test.user@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=incomplete_data)
    print(f"\nMissing credentials response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    try:
        test_register()
        test_login()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Please ensure the Flask server is running.")