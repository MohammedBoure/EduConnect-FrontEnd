import requests
import json

# Base URL of your Flask API (update if different)
BASE_URL = "http://localhost:5000/api"

# JWT token for authentication (replace with a valid token)
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTE0MzE5NywianRpIjoiNDI4NjUzMmItMWFmMC00MzM0LTkzNmQtZTA4MmI0MTU0MjYyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEyIiwibmJmIjoxNzQ1MTQzMTk3LCJjc3JmIjoiZjg3Mjk1NjItZTg2OC00NTZlLWFiNzItYTJkOWVlZTc5YTZhIiwiZXhwIjoxNzQ1MTQ0MDk3fQ.wO2rlRtkG41z05UKS8Tkgp6DJFZlaprpBEpL8m4JbzY"

# Headers with JWT token
headers = {
    "Authorization": f"Bearer {JWT_TOKEN}",
    "Content-Type": "application/json"
}

def test_search_profiles():
    print("\n=== Testing Profile Search API ===")
    try:
        # Test case 1: Search by name
        params = {"nom": "mohamad", "page": 11, "per_page": 5}
        response = requests.get(f"{BASE_URL}/search", headers=headers, params=params)
        print(f"Search by name 'mohamad': Status Code: {response.status_code}")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.json()}")

        # Test case 2: Search by filiere
        params = {"filiere": "Computer Science", "page": 1, "per_page": 5}
        response = requests.get(f"{BASE_URL}/search", headers=headers, params=params)
        print(f"\nSearch by filiere 'Computer Science': Status Code: {response.status_code}")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.json()}")

        # Test case 3: Search by competence
        params = {"competence": "Python", "page": 1, "per_page": 5}
        response = requests.get(f"{BASE_URL}/search", headers=headers, params=params)
        print(f"\nSearch by competence 'Python': Status Code: {response.status_code}")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.json()}")

        # Test case 4: Empty search (all profiles)
        params = {"page": 1, "per_page": 5}
        response = requests.get(f"{BASE_URL}/search", headers=headers, params=params)
        print(f"\nEmpty search: Status Code: {response.status_code}")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.json()}")

    except Exception as e:
        print(f"Exception occurred: {e}")

def test_send_message():
    print("\n=== Testing Send Message API ===")
    try:
        # Test case 1: Send a valid message
        data = {
            "receiver_id": 2,  # Replace with a valid receiver ID
            "content": "Hello, this is a test message!"
        }
        response = requests.post(f"{BASE_URL}/messages", headers=headers, json=data)
        print(f"Send valid message: Status Code: {response.status_code}")
        if response.status_code == 201:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.json()}")

        # Test case 2: Send message to self (should fail)
        data = {
            "receiver_id": 1,  # Replace with the current user's ID
            "content": "Trying to message myself"
        }
        response = requests.post(f"{BASE_URL}/messages", headers=headers, json=data)
        print(f"\nSend message to self: Status Code: {response.status_code}")
        if response.status_code == 400:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Unexpected response: {response.json()}")

        # Test case 3: Send message with missing content (should fail)
        data = {
            "receiver_id": 2
        }
        response = requests.post(f"{BASE_URL}/messages", headers=headers, json=data)
        print(f"\nSend message with missing content: Status Code: {response.status_code}")
        if response.status_code == 400:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Unexpected response: {response.json()}")

        # Test case 4: Send message to non-existent user (should fail)
        data = {
            "receiver_id": 9999,  # Non-existent user ID
            "content": "This should fail"
        }
        response = requests.post(f"{BASE_URL}/messages", headers=headers, json=data)
        print(f"\nSend message to non-existent user: Status Code: {response.status_code}")
        if response.status_code == 404:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Unexpected response: {response.json()}")

    except Exception as e:
        print(f"Exception occurred: {e}")

def test_get_messages():
    print("\n=== Testing Get Messages API ===")
    try:
        # Test case 1: Get messages with a valid user
        other_user_id = 2  # Replace with a valid user ID
        params = {"page": 1, "per_page": 10}
        response = requests.get(f"{BASE_URL}/messages/{other_user_id}", headers=headers, params=params)
        print(f"Get messages with user {other_user_id}: Status Code: {response.status_code}")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.json()}")

        # Test case 2: Get messages with non-existent user (should fail)
        other_user_id = 9999  # Non-existent user ID
        response = requests.get(f"{BASE_URL}/messages/{other_user_id}", headers=headers, params=params)
        print(f"\nGet messages with non-existent user {other_user_id}: Status Code: {response.status_code}")
        if response.status_code == 404:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Unexpected response: {response.json()}")

        # Test case 3: Get messages with pagination
        other_user_id = 2  # Replace with a valid user ID
        params = {"page": 2, "per_page": 5}
        response = requests.get(f"{BASE_URL}/messages/{other_user_id}", headers=headers, params=params)
        print(f"\nGet messages with pagination (page 2, per_page 5): Status Code: {response.status_code}")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.json()}")

    except Exception as e:
        print(f"Exception occurred: {e}")

def main():
    # Run all tests
    test_search_profiles()
    test_send_message()
    test_get_messages()

if __name__ == "__main__":
    main()