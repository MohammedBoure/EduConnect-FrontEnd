import requests

BASE_URL = "http://127.0.0.1:5000/api/search"

# أمثلة لطلبات بحث
search_params = [
    {},  # بدون أي فلاتر (إرجاع كل الحسابات)
    {'nom': 'Ali'},  # البحث بالاسم
    {'filiere': 'Informatique'},  # البحث بالفيلير
    {'nom': 'Ahmed', 'filiere': 'Mathématiques'}  # بحث مزدوج
]

for params in search_params:
    print(f"Searching with params: {params}")
    response = requests.get(BASE_URL, params=params)
    print("Status Code:", response.status_code)
    try:
        print("Response:", response.json())
    except Exception as e:
        print("Failed to parse response:", e)
    print("-" * 60)
