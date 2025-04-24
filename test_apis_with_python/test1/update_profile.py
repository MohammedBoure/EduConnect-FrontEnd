import requests
import json

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTMzMzk4NCwianRpIjoiYTI1MWY3Y2ItMjIzZi00ZGZlLWEwNWUtYjlmNjI2ZDkwZjE1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYiLCJuYmYiOjE3NDUzMzM5ODQsImNzcmYiOiJmMGFhMDY2My0wMmFiLTQxN2ItODZiYS05NTM3MTZkOGU3ZTMiLCJleHAiOjE3NDU0MjAzODR9.YDUShP7C7HZsFzHUjjekQCr-d55mZtuHwMV0kViJt_o"
user_id = 6
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

case = {
    "nom": "Ahmed Updated",
    "prenom": "Ben Ali Updated",
    "filiere": "Informatique Avancée",
    "competences": "Python, JavaScript, Java",
    "photo": "https://example.com/updated_photo.jpg"
}
    

url = f"http://localhost:5000/api/profile/{user_id}"
try:
    response = requests.put(url, headers=headers, data=json.dumps(case))
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
print("-" * 50)