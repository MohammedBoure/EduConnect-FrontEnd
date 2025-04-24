import requests
from faker import Faker
import random

fake = Faker()

URL = "http://localhost:5000/api/register" 

filieres = ["Informatique", "Mathématiques", "Physique", "Chimie"]
competences_possibles = ["Python", "Java", "C++", "SQL", "HTML", "CSS", "JavaScript"]

"""def generate_fake_user():
    return {
        "nom": fake.last_name(),
        "prenom": fake.first_name(),
        "email": fake.unique.email(),
        "mot_de_passe": "test1234",
        "filiere": random.choice(filieres),
        "competences": ", ".join(random.sample(competences_possibles, k=random.randint(1, 4)))
    }

for _ in range(4):  
    user = generate_fake_user()
    response = requests.post(URL, json=user)
    print(f"{response.status_code} - {response.json()}")
"""

user = {
        "nom": "aaaaa",
        "prenom": "aaaaa",
        "email": "aaaaa@gmail.com",
        "mot_de_passe": "aaaaa",
        "filiere": "aaaaa",
        "competences": ["python", "java", "c++"],
        "photo": "https://example.com/photo.jpg"
    }
response = requests.post(URL, json=user)
print(f"{response.status_code} - {response.json()}")