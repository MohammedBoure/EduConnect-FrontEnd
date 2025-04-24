import requests
import datetime
# === CONFIG ===
BASE_URL = "http://127.0.0.1:5000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTI3ODk3NCwianRpIjoiYWVlMDIxN2ItNDMzNS00YjJjLWI1MWMtODMyM2U2N2Q0ZjIwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQiLCJuYmYiOjE3NDUyNzg5NzQsImNzcmYiOiI1N2JkZjc3Yy03MjVjLTRhZDMtOGQ3Yi1jZjQ3YmFhODBlYWMiLCJleHAiOjE3NDUyNzk4NzR9.YTo5YNR0DmSb-SrvH2YvLnH55Mt17cmrJFUZpPuQpjk"
SENDER_ID = 4
RECEIVER_ID = 1  # Must be a valid user different from sender

# === PAYLOAD ===
payload = {
    "receiver_id": RECEIVER_ID,
    "content": f"Hello! This is a test message sent at.{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
}

# === HEADERS ===
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# === SEND REQUEST ===
try:
    response = requests.post(
        f"{BASE_URL}/api/messages",
        headers=headers,
        json=payload
    )

    # === HANDLE RESPONSE ===
    if response.status_code == 201:
        data = response.json()
        print("✅ Message sent successfully.")
        print(f"- ID: {data['sent_message']['id']}")
        print(f"- Content: {data['sent_message']['content']}")
        print(f"- From: {data['sent_message']['sender_id']} to {data['sent_message']['receiver_id']}")
        print(f"- Time: {data['sent_message']['created_at']}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"❌ Request failed: {e}")
