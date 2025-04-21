import requests
import json

# بيانات تسجيل الدخول
login_data = {
    "email": "ahmed@example.com",
    "mot_de_passe": "securepassword123"
}

# إرسال طلب POST
url = "http://localhost:5000/api/login"
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, headers=headers, data=json.dumps(login_data))
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")