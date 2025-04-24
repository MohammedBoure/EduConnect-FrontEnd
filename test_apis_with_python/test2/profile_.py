import requests
import json
import time

# إعدادات الخادم
BASE_URL = "http://127.0.0.1:5000"  # استبدل بـ "http://127.0.0.1:5000" لبيئة الاختبار
HEADERS = {"Content-Type": "application/json"}

# دوال مساعدة
def print_response(response, endpoint, method=""):
    print(f"\nTesting {method} {endpoint}:")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response (raw): {response.text}")

def get_jwt_token(email, password):
    """تسجيل الدخول للحصول على رمز JWT"""
    login_payload = {"email": email, "mot_de_passe": password}
    response = requests.post(f"{BASE_URL}/api/login", json=login_payload, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def create_test_user():
    """إنشاء مستخدم جديد للاختبار"""
    timestamp = int(time.time())
    user_data = {
        "nom": "Test",
        "prenom": "User",
        "email": f"test.user{timestamp}@example.com",
        "mot_de_passe": "SecurePass123",
        "filiere": "Informatique",
        "competences": ["Python", "JavaScript"],
        "photo": "https://example.com/photos/test.jpg"
    }
    response = requests.post(f"{BASE_URL}/api/register", json=user_data, headers=HEADERS)
    if response.status_code == 201:
        user_id = response.json()["user"]["id"]
        print_response(response, "/api/register", "POST")
        return user_data, user_id
    print_response(response, "/api/register", "POST")
    return None, None

# اختبار استرجاع ملف المستخدم
def test_get_profile(user_id, test_name):
    endpoint = f"/api/profile/{user_id}"
    print(f"\n=== {test_name} ===")
    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
    print_response(response, endpoint, "GET")
    return response

# اختبار تحديث ملف المستخدم
def test_update_profile(user_id, payload, jwt_token, test_name):
    endpoint = f"/api/profile/{user_id}"
    print(f"\n=== {test_name} ===")
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {jwt_token}"
    response = requests.put(f"{BASE_URL}{endpoint}", json=payload, headers=headers)
    print_response(response, endpoint, "PUT")
    return response

# اختبار حذف ملف المستخدم
def test_delete_profile(user_id, jwt_token, test_name):
    endpoint = f"/api/profile/{user_id}"
    print(f"\n=== {test_name} ===")
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {jwt_token}"
    response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers)
    print_response(response, endpoint, "DELETE")
    return response

# اختبار البحث عن ملفات المستخدمين
def test_search_profiles(params, jwt_token, test_name):
    endpoint = "/api/search"
    print(f"\n=== {test_name} ===")
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {jwt_token}"
    response = requests.get(f"{BASE_URL}{endpoint}", params=params, headers=headers)
    print_response(response, endpoint, "GET")
    return response

# تشغيل الاختبارات
def main():
    print("Starting Profile API Tests...\n")

    # إنشاء مستخدم جديد للاختبار
    print("=== Creating Test User ===")
    user_data, user_id = create_test_user()
    if not user_id:
        print("Failed to create test user. Exiting...")
        return

    # الحصول على رمز JWT
    jwt_token = get_jwt_token(user_data["email"], "SecurePass123")
    if not jwt_token:
        print("Failed to get JWT token. Exiting...")
        return

    # اختبار استرجاع ملف المستخدم
    print("\n=== Testing Get Profile Endpoint ===")
    test_get_profile(user_id, "Get Existing Profile")
    test_get_profile(9999, "Get Non-existent Profile")  # معرف غير موجود

    # اختبار تحديث ملف المستخدم
    print("\n=== Testing Update Profile Endpoint ===")
    update_payload = {
        "nom": "TestUpdated",
        "prenom": "UserUpdated",
        "filiere": "Génie Logiciel",
        "competences": ["Python", "Java"],
        "photo": "https://example.com/photos/updated.jpg"
    }
    test_update_profile(user_id, update_payload, jwt_token, "Valid Profile Update")
    
    # تحديث غير مصرح به (معرف مستخدم آخر)
    test_update_profile(user_id + 1, update_payload, jwt_token, "Unauthorized Profile Update")

    # اختبار البحث عن ملفات المستخدمين
    print("\n=== Testing Search Profiles Endpoint ===")
    search_params = {"nom": "TestUpdated", "page": 1, "per_page": 10}
    test_search_profiles(search_params, jwt_token, "Search by Name")
    
    search_params = {"competence": "Python", "page": 1, "per_page": 10}
    test_search_profiles(search_params, jwt_token, "Search by Competence")
    
    # اختبار البحث بدون مصادقة
    print("\n=== Testing Search Without Authentication ===")
    headers_no_auth = HEADERS.copy()
    response = requests.get(f"{BASE_URL}/api/search", params={"nom": "Test"}, headers=headers_no_auth)
    print_response(response, "/api/search", "GET")

    # اختبار حذف ملف المستخدم
    print("\n=== Testing Delete Profile Endpoint ===")
    test_delete_profile(user_id, jwt_token, "Delete Own Profile")
    test_delete_profile(user_id + 1, jwt_token, "Unauthorized Profile Deletion")

    print("\nProfile API Tests Completed!")

if __name__ == "__main__":
    main()