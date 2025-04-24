import requests

url = 'https://educonnect-wp9t.onrender.com/api/posts'

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTMzMTQ2OSwianRpIjoiOWNhZGI3NjgtMjE4NC00ZDU0LWE0ZWUtMmIxMjNjYWMwZTM5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjUiLCJuYmYiOjE3NDUzMzE0NjksImNzcmYiOiJlY2Q5NDM1Ny04ZTU4LTQwN2UtYWIxMS1kNzNlMGRlYzA0MjYiLCJleHAiOjE3NDU0MTc4Njl9.JsL7wY7Z2GSWwt8ta-upc3Qo1SGs7e8chpGRK2OAVK8'

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
