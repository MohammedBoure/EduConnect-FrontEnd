import requests

# === CONFIG ===
BASE_URL = "http://127.0.0.1:5000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTI3NTM0OSwianRpIjoiNDBhZjljOTQtODg3Yi00NTI2LThkMzAtYTJkODlmOWRiNzk4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQiLCJuYmYiOjE3NDUyNzUzNDksImNzcmYiOiJhNjdjYzRjMS0xZTk5LTRiYTMtOTczOC03OTIxNTYwY2EzYmQiLCJleHAiOjE3NDUyNzYyNDl9.CYjjgBdeT93tYb7F-1CgpsQ_sV-ZAAWUEpspZiXOX2k"
POST_ID = 1
NEW_CONTENT = "This is the updated content from test script."

# === HEADERS ===
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# === PAYLOAD ===
payload = {
    "content": NEW_CONTENT
}

# === REQUEST ===
response = requests.put(
    f"{BASE_URL}/api/posts/{POST_ID}",
    headers=headers,
    json=payload
)

# === RESULT ===
if response.status_code == 200:
    updated_post = response.json()['post']
    print("✅ Post updated successfully:")
    print(f"🆔 ID        : {updated_post['id']}")
    print(f"📝 Content   : {updated_post['content']}")
    print(f"👤 User ID   : {updated_post['user_id']}")
    print(f"📅 Created At: {updated_post['created_at']}")
else:
    print(f"❌ Error {response.status_code}: {response.text}")
