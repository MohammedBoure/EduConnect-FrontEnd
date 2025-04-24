import requests

url = 'http://localhost:5000/api/search'
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTI3NDEyNSwianRpIjoiZWU4YzdmYjQtY2U1MS00YzlkLTk4NDAtY2RhNjljMTkxNzZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQiLCJuYmYiOjE3NDUyNzQxMjUsImNzcmYiOiI5ZGVmNjY2OS1hOTZlLTQxYzQtYmUxMC1mYmY4ZjllNWM3NjAiLCJleHAiOjE3NDUyNzUwMjV9.UpIQLQTfW4yrMNXiBx1W0filQLSimwvdY0asEi4vquc"

params = {
    'filiere': 'Physique',
}

headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print("Résultats:", data['results'])
    print("Total:", data['total'])
    print("Page:", data['page'])
else:
    print("Erreur:", response.status_code, response.text)
