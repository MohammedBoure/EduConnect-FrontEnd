import requests

# معلومات الطلب
user_id = 1  # غيّر هذا إلى ID المستخدم المناسب للاختبار
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTEzNTIxMCwianRpIjoiNWY0NGQ4ZWYtMmZhNy00ZjAxLTljNGYtMzM5NWJjMzk3N2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDUxMzUyMTAsImNzcmYiOiIxNTZhNWM3Mi0zZTI3LTQzMTUtOTNiYS00NTYxNDA0MDRkYmUiLCJleHAiOjE3NDUxMzYxMTB9.nfbXYU6RJS41VR-qDMB7jMZwjeU_y_AtvOghi1K1xJQ"

# رابط الـ API (غيّره إذا كنت تستخدم بيئة مختلفة)
url = f"http://127.0.0.1:5000/api/profile/{user_id}"

# ترويسة المصادقة
headers = {
    "Authorization": f"Bearer {token}"
}

# إرسال الطلب
response = requests.delete(url, headers=headers)

# عرض النتيجة
print(f"Status Code: {response.status_code}")
print("Response:", response.json())
