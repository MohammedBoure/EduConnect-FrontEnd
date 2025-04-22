import requests

url = 'http://localhost:5000/api/posts'

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTI3NTM0OSwianRpIjoiNDBhZjljOTQtODg3Yi00NTI2LThkMzAtYTJkODlmOWRiNzk4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQiLCJuYmYiOjE3NDUyNzUzNDksImNzcmYiOiJhNjdjYzRjMS0xZTk5LTRiYTMtOTczOC03OTIxNTYwY2EzYmQiLCJleHAiOjE3NDUyNzYyNDl9.CYjjgBdeT93tYb7F-1CgpsQ_sV-ZAAWUEpspZiXOX2k"

data = {
    'content': 'Hello, this is my first post!'
}

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    print("✅ Post created:", response.json()['post'])
elif response.status_code == 400:
    print("⚠️ Validation error:", response.json())
elif response.status_code == 401:
    print("🔒 Authentication error:", response.json())
else:
    print("❌ Server error:", response.status_code, response.text)
