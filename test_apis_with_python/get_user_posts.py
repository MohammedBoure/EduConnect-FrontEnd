# test_get_user_posts.py
import requests

BASE_URL = "http://127.0.0.1:5000"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTI3NjM4MSwianRpIjoiMmI4OTEyMDMtZWQ5Ni00MjkzLWE5NzUtZmUxMGY1MWNhZjcxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQiLCJuYmYiOjE3NDUyNzYzODEsImNzcmYiOiI3YTQ2NDAzZi0wZDBjLTQzNjAtODIxNi0zZTJjMDNjMGRiN2EiLCJleHAiOjE3NDUyNzcyODF9.jhQEVt1v3uMTmIr178s82i_DEH8i0wl66wxESXs0syY"

USER_ID = 4

params = {
    "page":1,
    "per_page": 3
}

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(
    f"{BASE_URL}/api/posts/user/{USER_ID}",
    headers=headers,
    params=params
)

if response.status_code == 200:
    data = response.json()
    print("✅ Posts retrieved successfully.")
    for post in data['posts']:
        print(f"- {post['content']} (by {post['author']['prenom']} {post['author']['nom']})")
else:
    print(f"❌ Error {response.status_code}: {response.text}")
