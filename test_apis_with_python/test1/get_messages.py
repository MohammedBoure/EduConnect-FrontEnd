import requests

url = 'http://localhost:5000/api/messages'  
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTI3OTEzMSwianRpIjoiNGQzOWFlYjEtMTRjNC00NDNjLWExNGYtZTczZDgyOGE5OTY1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDUyNzkxMzEsImNzcmYiOiJlNThkMmRhYy01NmIyLTQ0YjQtYTI3Mi0yZThjYmQ5YzJiZDgiLCJleHAiOjE3NDUyODAwMzF9.fhot0Q63t4HhnlAR8b48YCd_equJsq2JufUUmvhn9pU"

other_user_id = 4  

params = {
    'page': 1,
    'per_page': 30
}

headers = {
    'Authorization': f'Bearer {token}'  
}

response = requests.get(f'{url}/{other_user_id}', params=params, headers=headers)

if response.status_code == 200:
    print("Messages fetched successfully!")
    print(response.json()) 
else:
    print(f"Error {response.status_code}: {response.json()}")
