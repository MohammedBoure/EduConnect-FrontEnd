import requests
import json

login_data = {
    "email": "aaaaa@gmail.com",
    "mot_de_passe": "aaaaa"
}

url = "http://localhost:5000/api/login"
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, headers=headers, data=json.dumps(login_data))
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")