import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"
HEADERS = {"Content-Type": "application/json"}

def print_response(response):
    """Helper function to print the response status and body."""
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print("-" * 50)

print("GET /admin/users/7")
response = requests.get(f"{BASE_URL}/admin/users/7", headers=HEADERS)
print_response(response)