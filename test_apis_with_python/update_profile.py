import requests
import json

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTEzNTIxMCwianRpIjoiNWY0NGQ4ZWYtMmZhNy00ZjAxLTljNGYtMzM5NWJjMzk3N2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDUxMzUyMTAsImNzcmYiOiIxNTZhNWM3Mi0zZTI3LTQzMTUtOTNiYS00NTYxNDA0MDRkYmUiLCJleHAiOjE3NDUxMzYxMTB9.nfbXYU6RJS41VR-qDMB7jMZwjeU_y_AtvOghi1K1xJQ"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

test_cases = [
    {
        "user_id": 1,
        "data": {
            "nom": "Ahmed Updated",
            "prenom": "Ben Ali Updated",
            "filiere": "Informatique Avancée",
            "competences": "Python, JavaScript, Java",
            "photo": "https://example.com/updated_photo.jpg"
        },
        "description": "تحديث صحيح لملف المستخدم 1"
    },
    {
        "user_id": 2,
        "data": {"nom": "Unauthorized User"},
        "description": "محاولة تحديث ملف مستخدم آخر (غير مصرح)"
    },
    {
        "user_id": 1,
        "data": {},
        "description": "إرسال بيانات فارغة"
    },
    {
        "user_id": 999,
        "data": {"nom": "Nonexistent User"},
        "description": "محاولة تحديث مستخدم غير موجود"
    },
    {
        "user_id": 1,
        "data": {"nom": "Ahmed Partial Update"},
        "description": "تحديث جزئي (حقل واحد فقط)"
    }
]

for case in test_cases:
    url = f"http://localhost:5000/api/profile/{case['user_id']}"
    print(f"Testing: {case['description']}")
    try:
        response = requests.put(url, headers=headers, data=json.dumps(case['data']))
        print("Status Code:", response.status_code)
        print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    print("-" * 50)