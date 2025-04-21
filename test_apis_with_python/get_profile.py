import requests

# عنوان الـ endpoint مع معرف المستخدم (user_id)
user_id = 1  # يمكنك تغيير هذا إلى معرف المستخدم المطلوب
url = f"http://localhost:5000/api/profile/{user_id}"

try:
    # إرسال طلب GET
    response = requests.get(url)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")