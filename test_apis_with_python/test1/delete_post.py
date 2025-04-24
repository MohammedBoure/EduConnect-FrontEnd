import requests

# === CONFIG ===
BASE_URL = "http://127.0.0.1:5000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTI3NzEwMywianRpIjoiYzgxN2VjMjUtZDFiZS00ZWJmLWE3YWYtYTg3YmZhNmI4MTg0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQiLCJuYmYiOjE3NDUyNzcxMDMsImNzcmYiOiIyMWI5NDBjZi02MTk4LTQ3MWMtOTZiZi1kNjU4MjEzODZjN2YiLCJleHAiOjE3NDUyNzgwMDN9.Dj8rvVNqM-bJF3h61opDf5OWT7-X_v4c07FBAQzHq3o"
POST_ID = 3

# === HEADERS ===
headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# === REQUEST ===
response = requests.delete(
    f"{BASE_URL}/api/posts/{POST_ID}",
    headers=headers
)

# === RESULT ===
if response.status_code == 200:
    print("✅ Post deleted successfully.")
else:
    print(f"❌ Error {response.status_code}: {response.text}")
