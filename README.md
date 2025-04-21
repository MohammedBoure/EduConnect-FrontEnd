EduConnect Backend API
EduConnect is a Flask-based backend API for a student networking platform, enabling user registration, profile management, messaging, and post creation. It uses SQLAlchemy for database operations, JWT for authentication, and SQLite for data storage (configurable for other databases in production).
Deployed API: https://educonnect-wp9t.onrender.com

Table of Contents

Features
Technologies
Installation
Usage
API Endpoints
Authentication
User Registration
User Login
Profile Management
Profile Search
Messaging
Posts


Error Handling
Contributing
License


Features

User authentication with JWT
Profile creation, update, and deletion
Search profiles by name, field of study, or skills
Private messaging between users
Post creation and management
Pagination for search results, messages, and posts
CORS support for frontend integration


Technologies

Flask: Web framework
SQLAlchemy: ORM for database management
Flask-JWT-Extended: JWT authentication
SQLite: Default database (configurable for PostgreSQL, etc.)
Flask-CORS: Cross-origin resource sharing
Python 3.8+


Installation

Clone the repository:
git clone https://github.com/your-username/educonnect-backend.git
cd educonnect-backend


Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt

Example requirements.txt:
flask==2.3.3
flask-sqlalchemy==3.0.5
flask-jwt-extended==4.5.3
flask-cors==4.0.0
werkzeug==3.0.1


Configure environment:
Create a .env file or update app.py with:
JWT_SECRET_KEY=your-super-secret-and-long-key
SQLALCHEMY_DATABASE_URI=sqlite:///student_directory.db


Run the application:
python app.py

The API will be available at http://localhost:5000/api.



Usage
To interact with the API:

Use tools like Postman or cURL to send HTTP requests.

Authenticate via /api/login to obtain a JWT token.

Include the token in the Authorization header for protected endpoints:
Authorization: Bearer <your_access_token>



Example: Register a new user:
curl -X POST https://educonnect-wp9t.onrender.com/api/register \
-H "Content-Type: application/json" \
-d '{
  "nom": "Doe",
  "prenom": "John",
  "email": "john.doe@example.com",
  "mot_de_passe": "securepassword",
  "filiere": "Computer Science",
  "competences": ["Python", "JavaScript"]
}'


API Endpoints
Base URL: https://educonnect-wp9t.onrender.com/api
Authentication
Most endpoints require a JWT token in the Authorization header.
User Registration

POST /register

Description: Register a new user.

Body:
{
  "nom": "string",
  "prenom": "string",
  "email": "string",
  "mot_de_passe": "string",
  "filiere": "string",
  "competences": ["string"],
  "photo": "string" (optional)
}


Response (201):
{
  "message": "User registered successfully",
  "user": {
    "id": integer,
    "nom": "string",
    "prenom": "string",
    "email": "string"
  }
}



User Login

POST /login

Description: Authenticate and get a JWT token.

Body:
{
  "email": "string",
  "mot_de_passe": "string"
}


Response (200):
{
  "access_token": "string",
  "user_id": integer
}



Profile Management

GET /profile/<user_id>

Description: Get a user's profile.

Response (200):
{
  "id": integer,
  "nom": "string",
  "prenom": "string",
  "email": "string",
  "filiere": "string",
  "competences": ["string"],
  "photo": "string" | null
}


PUT /profile/<user_id> (Authenticated)

Description: Update own profile.

Body (optional fields):
{
  "nom": "string",
  "prenom": "string",
  "filiere": "string",
  "competences": ["string"],
  "photo": "string"
}


DELETE /profile/<user_id> (Authenticated)

Description: Delete own profile.

Response (200):
{
  "message": "Profile deleted successfully"
}



Profile Search

GET /search (Authenticated)

Description: Search profiles by name, field, or skill.

Query Parameters:

nom: Name (first or last)
filiere: Field of study
competence: Skill
page: Page number (default: 1)
per_page: Results per page (default: 10)


Response (200):
{
  "results": [
    {
      "id": integer,
      "nom": "string",
      "prenom": "string",
      "filiere": "string",
      "competences": ["string"],
      "photo": "string" | null
    }
  ],
  "total": integer,
  "page": integer,
  "pages": integer,
  "per_page": integer
}



Messaging

POST /messages (Authenticated)

Description: Send a message to another user.

Body:
{
  "receiver_id": integer,
  "content": "string"
}


Response (201):
{
  "message": "Message sent successfully",
  "sent_message": {
    "id": integer,
    "content": "string",
    "sender_id": integer,
    "receiver_id": integer,
    "created_at": "string"
  }
}


GET /messages/<other_user_id> (Authenticated)

Description: Get messages with another user.

Query Parameters:

page: Page number (default: 1)
per_page: Messages per page (default: 30)


Response (200):
{
  "messages": [
    {
      "id": integer,
      "content": "string",
      "sender_id": integer,
      "receiver_id": integer,
      "created_at": "string"
    }
  ],
  "total": integer,
  "page": integer,
  "pages": integer,
  "per_page": integer
}



Posts

POST /posts (Authenticated)

Description: Create a new post.

Body:
{
  "content": "string"
}


Response (201):
{
  "message": "Post created successfully",
  "post": {
    "id": integer,
    "content": "string",
    "created_at": "string",
    "user_id": integer
  }
}


GET /posts/user/<user_id> (Authenticated)

Description: Get a user's posts.

Query Parameters:

page: Page number (default: 1)
per_page: Posts per page (default: 10)


Response (200):
{
  "posts": [
    {
      "id": integer,
      "content": "string",
      "created_at": "string",
      "user_id": integer,
      "author": {
        "nom": "string",
        "prenom": "string"
      }
    }
  ],
  "total": integer,
  "page": integer,
  "pages": integer,
  "per_page": integer
}


PUT /posts/<post_id> (Authenticated)

Description: Update own post.

Body:
{
  "content": "string"
}


DELETE /posts/<post_id> (Authenticated)

Description: Delete own post.

Response (200):
{
  "message": "Post deleted successfully"
}




Error Handling
Errors are returned in JSON format:
{
  "error": "string"
}

Common status codes:

200 OK: Success
201 Created: Resource created
400 Bad Request: Invalid input
401 Unauthorized: Invalid/missing token
403 Forbidden: Unauthorized action
404 Not Found: Resource not found
409 Conflict: Resource exists (e.g., email)
500 Internal Server Error: Server error


Contributing

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a Pull Request.

Please follow the Code of Conduct and include tests for new features.

License
This project is licensed under the MIT License. See the LICENSE file for details.

For more details, visit the deployed API at https://educonnect-wp9t.onrender.com or check out xAI's API documentation at https://x.ai/api.
