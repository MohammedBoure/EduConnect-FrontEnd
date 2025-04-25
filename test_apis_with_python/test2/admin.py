import requests
import json
from datetime import datetime

BASE_URL = "https://educonnect-wp9t.onrender.com/api"
HEADERS = {"Content-Type": "application/json"}

def print_response(response):
    """Helper function to print the response status and body."""
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print("-" * 50)

# --- User Management Requests ---

# GET /admin/users (List users with pagination)
print("GET /admin/users")
response = requests.get(f"{BASE_URL}/admin/users", params={"page": 1, "per_page": 10}, headers=HEADERS)
print_response(response)

# GET /admin/users/1 (Get specific user)
print("GET /admin/users/3")
response = requests.get(f"{BASE_URL}/admin/users/3", headers=HEADERS)
print_response(response)

# PUT /admin/users/1 (Update user)
print("PUT /admin/users/1")
update_user_data = {
    "last_name": "Smith",
    "first_name": "Jane",
    "email": "jani.smith@example.com",
    "department": "HR",
    "skills": ["Python", "Java"],
    "photo": "new_photo.jpg",
    "role": "admin"
}
response = requests.put(f"{BASE_URL}/admin/users/2", data=json.dumps(update_user_data), headers=HEADERS)
print_response(response)

# DELETE /admin/users/1 (Delete user)
"""print("DELETE /admin/users/1")
response = requests.delete(f"{BASE_URL}/admin/users/2", headers=HEADERS)
print_response(response)"""

# --- Post Management Requests ---

# POST /admin/posts/create (Create a post)
print("POST /admin/posts/create")
create_post_data = {
    "user_id": 3,
    "title": "Test Post Title",
    "content": "This is a test post created by admin.",
    "image": None
}
response = requests.post(f"{BASE_URL}/admin/posts/create", data=json.dumps(create_post_data), headers=HEADERS)
print_response(response)

id_post = response.json()["post"]["id"]
# GET /admin/posts (List posts with pagination)
print("GET /admin/posts")
response = requests.get(f"{BASE_URL}/admin/posts", params={"page": 1, "per_page": 10}, headers=HEADERS)
print_response(response)

# PUT /admin/posts/2 (Update post)
print(f"PUT /admin/posts/{id_post}")
update_post_data = {
    "title": "Updated Post Title",
    "content": "Updated post content by admin."
}
response = requests.put(f"{BASE_URL}/admin/posts/{id_post}", data=json.dumps(update_post_data), headers=HEADERS)
print_response(response)

# DELETE /admin/posts/2 (Delete post)
"""print("DELETE /admin/posts/2")
response = requests.delete(f"{BASE_URL}/admin/posts/2", headers=HEADERS)
print_response(response)
"""
# --- Comment Management Requests ---

# POST /admin/posts/2/comments (Add comment to post)
print(f"POST /admin/posts/{id_post}/comments")
add_comment_data = {
    "content": "This is a test comment.",
    "created_at": datetime.utcnow().isoformat()
}
response = requests.post(f"{BASE_URL}/admin/posts/{id_post}/comments", data=json.dumps(add_comment_data), headers=HEADERS)
print_response(response)

id_comment = response.json()["comment"]["id"]

# GET /admin/comments (List comments with pagination)
print("GET /admin/comments")
response = requests.get(f"{BASE_URL}/admin/comments", params={"page": 1, "per_page": 20}, headers=HEADERS)
print_response(response)

# PUT /admin/comments/1 (Update comment)
print(f"PUT /admin/comments/{id_comment}")
update_comment_data = {
    "content": "Updated comment content by admin."
}
response = requests.put(f"{BASE_URL}/admin/comments/{id_comment}", data=json.dumps(update_comment_data), headers=HEADERS)
print_response(response)

# DELETE /admin/comments/3 (Delete comment)
"""print("DELETE /admin/comments/3")
response = requests.delete(f"{BASE_URL}/admin/comments/3", headers=HEADERS)
print_response(response)"""

# --- Message Management Requests ---

# POST /admin/messages (Send message)
print("POST /admin/messages")
send_message_data = {
    "sender_id": 3,
    "receiver_id": 2,
    "content": "Hello, this is a test message from admin."
}
response = requests.post(f"{BASE_URL}/admin/messages", data=json.dumps(send_message_data), headers=HEADERS)
print_response(response)

# POST /admin/messages/2 (Get messages between users)
print("POST /admin/messages/2")
get_messages_data = {
    "user_id": 2
}
response = requests.post(f"{BASE_URL}/admin/messages/2", data=json.dumps(get_messages_data), headers=HEADERS, params={"page": 1, "per_page": 30})
print_response(response)

# GET /admin/messages (List messages with pagination)
print("GET /admin/messages")
response = requests.get(f"{BASE_URL}/admin/messages", params={"page": 1, "per_page": 30}, headers=HEADERS)
print_response(response)

# DELETE /admin/messages/1 (Delete message)
"""print("DELETE /admin/messages/1")
response = requests.delete(f"{BASE_URL}/admin Messages/ ", headers=HEADERS)
print_response(response)"""