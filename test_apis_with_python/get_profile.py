import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTI3MTc4NSwianRpIjoiZWU3Y2VlNjQtNTNlYi00NTgwLWFmMjgtZTA5NTgzODQ5ZjE0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDUyNzE3ODUsImNzcmYiOiI1N2Y5MDAxMi1mNjRmLTRjOWMtYjg0MS1lZTU1Mzc1OGY4YzkiLCJleHAiOjE3NDUyNzI2ODV9.BubwyTAhOewW_0OdSaKPxfqsZOWJ4L8PXYlEhNWmG9Y"
user_id = 1
url = f"http://localhost:5000/api/profile/{user_id}"

headers = {
    "Authorization": f"Bearer {token}"
}

try:
    response = requests.get(url, headers=headers)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")