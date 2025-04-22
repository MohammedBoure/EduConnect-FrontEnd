import requests


user_id = 2  
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTI3MjY4OSwianRpIjoiNWRlOWMxMzMtNTJjZS00MzJhLWEyY2MtZDA4MGMwYzBkNmUxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3NDUyNzI2ODksImNzcmYiOiJkMDIxNjZmOC05Mjk0LTQ3NzMtYTNlMi1kM2JhNTAzOWMxOTgiLCJleHAiOjE3NDUyNzM1ODl9.LwlH--9UwMz2J9PNe_7reyypk0lJO1bdBO7-ob5f5L4"

url = f"http://127.0.0.1:5000/api/profile/{user_id}"

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.delete(url, headers=headers)

print(f"Status Code: {response.status_code}")
print("Response:", response.json())
