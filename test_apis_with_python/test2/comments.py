import requests

# URL الخاص بحذف التعليق
url = 'http://127.0.0.1:5000/api/admin/comments/2'  # تأكد من أن comment_id هو 2 أو الرقم الذي ترغب في حذفه

# إرسال طلب DELETE لحذف التعليق
response = requests.delete(url)

# طباعة حالة الاستجابة والبيانات المرتبطة بها
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("Response JSON:", response.json())
else:
    print("Error:", response.json())
