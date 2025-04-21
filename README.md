EduConnect Backend API Documentation
This document provides detailed information about the EduConnect Backend API, which powers a student directory and networking platform. The API allows users to register, log in, manage profiles, search for other users, send messages, and create posts. It is built using Flask, SQLAlchemy, and JWT for authentication, with an SQLite database for data storage.
The base URL for the API is: https://educonnect-wp9t.onrender.com/api
Table of Contents

Authentication
API Endpoints
User Registration
User Login
Profile Management
Profile Search
Messaging
Posts


Error Handling
Setup and Deployment


Authentication
Most endpoints require authentication using a JSON Web Token (JWT). To authenticate:

Obtain a token by sending a POST request to /api/login with valid credentials.

Include the token in the Authorization header for protected endpoints:
Authorization: Bearer <your_access_token>




API Endpoints
User Registration
Endpoint: POST /api/register
Description: Registers a new user in the system.
Request Body:
{
  "nom": "string",
  "prenom": "string",
  "email": "string",
  "mot_de_passe": "string",
  "filiere": "string",
  "competences": ["string"] | "string",
  "photo": "string" (optional)
}

Response:

201 Created:
{
  "message": "User registered successfully",
  "user": {
    "id": integer,
    "nom": "string",
    "prenom": "string",
    "email": "string"
  }
}


400 Bad Request: Missing or empty required fields.

409 Conflict: Email already exists.

500 Internal Server Error: Database or unexpected error.


Example:
curl -X POST https://educonnect-wp9t.onrender.com/api/register \
-H "Content-Type: application/json" \
-d '{
  "nom": "Doe",
  "prenom": "John",
  "email": "john.doe@example.com",
  "mot_de_passe": "securepassword",
  "filiere": "Computer Science",
  "competences": ["Python", "JavaScript"],
  "photo": "https://example.com/photo.jpg"
}'


User Login
Endpoint: POST /api/login
Description: Authenticates a user and returns a JWT token.
Request Body:
{
  "email": "string",
  "mot_de_passe": "string"
}

Response:

200 OK:
{
  "access_token": "string",
  "user_id": integer
}


400 Bad Request: Missing email or password.

401 Unauthorized: Invalid email or password.


Example:
curl -X POST https://educonnect-wp9t.onrender.com/api/login \
-H "Content-Type: application/json" \
-d '{
  "email": "john.doe@example.com",
  "mot_de_passe": "securepassword"
}'


Profile Management
Get Profile
Endpoint: GET /api/profile/<user_id>
Description: Retrieves a user's profile by ID. Requires authentication.
Headers:

Authorization: Bearer <token>

Response:

200 OK:
{
  "id": integer,
  "nom": "string",
  "prenom": "string",
  "email": "string",
  "filiere": "string",
  "competences": ["string"],
  "photo": "string" | null
}


404 Not Found: User not found.


Example:
curl -X GET https://educonnect-wp9t.onrender.com/api/profile/1 \
-H "Authorization: Bearer <token>"

Update Profile
Endpoint: PUT /api/profile/<user_id>
Description: Updates the authenticated user's profile. Only the user can update their own profile.
Headers:

Authorization: Bearer <token>

Request Body (all fields optional):
{
  "nom": "string",
  "prenom": "string",
  "filiere": "string",
  "competences": ["string"] | "string",
  "photo": "string"
}

Response:

200 OK:
{
  "message": "Profile updated successfully",
  "user": {
    "id": integer,
    "nom": "string",
    "prenom": "string",
    "filiere": "string",
    "competences": ["string"],
    "photo": "string" | null
  }
}


400 Bad Request: No update data provided.

401 Unauthorized: Invalid token.

403 Forbidden: Attempt to update another user's profile.

404 Not Found: User not found.

500 Internal Server Error: Database or unexpected error.


Example:
curl -X PUT https://educonnect-wp9t.onrender.com/api/profile/1 \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{
  "nom": "Doe",
  "prenom": "Jane",
  "filiere": "Data Science",
  "competences": ["Python", "SQL"]
}'

Delete Profile
Endpoint: DELETE /api/profile/<user_id>
Description: Deletes the authenticated user's profile and associated data (posts, messages).
Headers:

Authorization: Bearer <token>

Response:

200 OK:
{
  "message": "Profile deleted successfully"
}


401 Unauthorized: Invalid token.

403 Forbidden: Attempt to delete another user's profile.

404 Not Found: User not found.

500 Internal Server Error: Database or unexpected error.


Example:
curl -X DELETE https://educonnect-wp9t.onrender.com/api/profile/1 \
-H "Authorization: Bearer <token>"


Profile Search
Endpoint: GET /api/search
Description: Searches for user profiles by name, field of study, or competence. Supports pagination.
Headers:

Authorization: Bearer <token>

Query Parameters:

nom (optional): Search by name (first or last).
filiere (optional): Search by field of study.
competence (optional): Search by competence.
page (optional, default: 1): Page number.
per_page (optional, default: 10): Results per page.

Response:

200 OK:
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



Example:
curl -X GET "https://educonnect-wp9t.onrender.com/api/search?nom=John&filiere=Computer%20Science&competence=Python&page=1&per_page=10" \
-H "Authorization: Bearer <token>"


Messaging
Send Message
Endpoint: POST /api/messages
Description: Sends a message from the authenticated user to another user.
Headers:

Authorization: Bearer <token>

Request Body:
{
  "receiver_id": integer,
  "content": "string"
}

Response:

201 Created:
{
  "message": "Message sent successfully",
  "sent_message": {
    "id": integer,
    "content": "string",
    "sender_id": integer,
    "receiver_id": integer,
    "created_at": "string" (ISO format)
  }
}


400 Bad Request: Missing or invalid receiver_id or content.

401 Unauthorized: Invalid token.

404 Not Found: Receiver not found.

500 Internal Server Error: Database or unexpected error.


Example:
curl -X POST https://educonnect-wp9t.onrender.com/api/messages \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{
  "receiver_id": 2,
  "content": "Hello, let's collaborate!"
}'

Get Messages
Endpoint: GET /api/messages/<other_user_id>
Description: Retrieves messages between the authenticated user and another user. Supports pagination.
Headers:

Authorization: Bearer <token>

Query Parameters:

page (optional, default: 1): Page number.
per_page (optional, default: 30): Messages per page.

Response:

200 OK:
{
  "messages": [
    {
      "id": integer,
      "content": "string",
      "sender_id": integer,
      "receiver_id": integer,
      "created_at": "string" (ISO format)
    }
  ],
  "total": integer,
  "page": integer,
  "pages": integer,
  "per_page": integer
}


401 Unauthorized: Invalid token.

404 Not Found: Other user not found.

500 Internal Server Error: Database or unexpected error.


Example:
curl -X GET "https://educonnect-wp9t.onrender.com/api/messages/2?page=1&per_page=30" \
-H "Authorization: Bearer <token>"


Posts
Create Post
Endpoint: POST /api/posts
Description: Creates a new post by the authenticated user.
Headers:

Authorization: Bearer <token>

Request Body:
{
  "content": "string"
}

Response:

201 Created:
{
  "message": "Post created successfully",
  "post": {
    "id": integer,
    "content": "string",
    "created_at": "string" (ISO format),
    "user_id": integer
  }
}


400 Bad Request: Missing or empty content.

401 Unauthorized: Invalid token.

500 Internal Server Error: Database or unexpected error.


Example:
curl -X POST https://educonnect-wp9t.onrender.com/api/posts \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{
  "content": "Excited to share my new project!"
}'

Get User Posts
Endpoint: GET /api/posts/user/<user_id>
Description: Retrieves posts by a specific user. Supports pagination.
Headers:

Authorization: Bearer <token>

Query Parameters:

page (optional, default: 1): Page number.
per_page (optional, default: 10): Posts per page.

Response:

200 OK:
{
  "posts": [
    {
      "id": integer,
      "content": "string",
      "created_at": "string" (ISO format),
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


404 Not Found: User not found.

500 Internal Server Error: Database or unexpected error.


Example:
curl -X GET "https://educonnect-wp9t.onrender.com/api/posts/user/1?page=1&per_page=10" \
-H "Authorization: Bearer <token>"

Update Post
Endpoint: PUT /api/posts/<post_id>
Description: Updates a post by the authenticated user (only their own posts).
Headers:

Authorization: Bearer <token>

Request Body:
{
  "content": "string"
}

Response:

200 OK:
{
  "message": "Post updated successfully",
  "post": {
    "id": integer,
    "content": "string",
    "created_at": "string" (ISO format),
    "user_id": integer
  }
}


400 Bad Request: Missing or empty content.

401 Unauthorized: Invalid token.

403 Forbidden: Attempt to update another user's post.

404 Not Found: Post not found.

500 Internal Server Error: Database or unexpected error.


Example:
curl -X PUT https://educonnect-wp9t.onrender.com/api/posts/1 \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{
  "content": "Updated project details!"
}'

Delete Post
Endpoint: DELETE /api/posts/<post_id>
Description: Deletes a post by the authenticated user (only their own posts).
Headers:

Authorization: Bearer <token>

Response:

200 OK:
{
  "message": "Post deleted successfully"
}


401 Unauthorized: Invalid token.

403 Forbidden: Attempt to delete another user's post.

404 Not Found: Post not found.

500 Internal Server Error: Database or unexpected error.


Example:
curl -X DELETE https://educonnect-wp9t.onrender.com/api/posts/1 \
-H "Authorization: Bearer <token>"


Error Handling
All endpoints return errors in a consistent JSON format:
{
  "error": "string"
}

Common HTTP status codes:

200 OK: Request successful.
201 Created: Resource created successfully.
400 Bad Request: Invalid or missing input.
401 Unauthorized: Invalid or missing authentication token.
403 Forbidden: User not authorized to perform the action.
404 Not Found: Resource not found.
409 Conflict: Resource already exists (e.g., email during registration).
500 Internal Server Error: Server-side error.


Setup and Deployment
Local Development

Clone the repository and install dependencies:
pip install flask flask-sqlalchemy flask-jwt-extended werkzeug flask-cors


Set the JWT_SECRET_KEY in the application configuration (replace the placeholder).

Run the application:
python app.py


The API will be available at http://localhost:5000/api.


Production Deployment
The API is deployed at https://educonnect-wp9t.onrender.com. Ensure the following:

Use a secure JWT_SECRET_KEY.
Replace the SQLite database with a production-ready database (e.g., PostgreSQL).
Configure CORS to allow specific origins instead of *.
Use a WSGI server like Gunicorn for better performance.

For further details on the API service, visit xAI API.

This README provides a comprehensive guide for frontend developers to integrate with the EduConnect Backend API. For additional support, refer to the deployed application at https://educonnect-wp9t.onrender.com.
