
## API Endpoints

### User Registration

*   **Endpoint:** `POST /api/register`
*   **Description:** Registers a new user.
*   **Request Body:**
    ```json
    {
      "nom": "string",
      "prenom": "string",
      "email": "string",
      "mot_de_passe": "string",
      "filiere": "string",
      "competences": ["string"],
      "photo": "string"
    }
    ```
*   **Success Response (`201 Created`):** User details (id, nom, prenom, email).
*   **Common Errors:** `400 Bad Request` (missing fields), `409 Conflict` (email exists).

### User Login

*   **Endpoint:** `POST /api/login`
*   **Description:** Authenticates a user and returns a JWT token and user ID.
*   **Request Body:**
    ```json
    {
      "email": "string",
      "mot_de_passe": "string"
    }
    ```
*   **Success Response (`200 OK`):**
    ```json
    {
      "access_token": "string",
      "user_id": "integer"
    }
    ```
*   **Common Errors:** `400 Bad Request` (missing fields), `401 Unauthorized` (invalid credentials).

### Profile Management

#### Get Profile

*   **Endpoint:** `GET /api/profile/<user_id>`
*   **Auth:** Required.
*   **Description:** Retrieves a user's profile.
*   **Success Response (`200 OK`):** User profile details (id, nom, prenom, email, filiere, competences, photo).
*   **Common Errors:** `404 Not Found` (user not found).

#### Update Profile

*   **Endpoint:** `PUT /api/profile/<user_id>`
*   **Auth:** Required. Only the user can update their own profile.
*   **Description:** Updates the authenticated user's profile.
*   **Request Body (all fields optional):**
    ```json
    {
      "nom": "string",
      "prenom": "string",
      "filiere": "string",
      "competences": ["string"],
      "photo": "string"
    }
    ```
*   **Success Response (`200 OK`):** Updated user profile details.
*   **Common Errors:** `400 Bad Request` (no data), `401 Unauthorized`, `403 Forbidden` (not own profile), `404 Not Found`.

#### Delete Profile

*   **Endpoint:** `DELETE /api/profile/<user_id>`
*   **Auth:** Required. Only the user can delete their own profile.
*   **Description:** Deletes the authenticated user's profile and associated data.
*   **Success Response (`200 OK`):** Confirmation message.
*   **Common Errors:** `401 Unauthorized`, `403 Forbidden`, `404 Not Found`.

### Profile Search

*   **Endpoint:** `GET /api/search`
*   **Auth:** Required.
*   **Description:** Searches user profiles with pagination.
*   **Query Parameters:**
    *   `nom` (optional): Search by name.
    *   `filiere` (optional): Search by field of study.
    *   `competence` (optional): Search by competence.
    *   `page` (optional, default: 1): Page number.
    *   `per_page` (optional, default: 10): Results per page.
*   **Success Response (`200 OK`):** Paginated list of matching user profiles.
    ```json
    {
      "results": [ "/* user profiles */" ],
      "total": "integer",
      "page": "integer",
      "pages": "integer",
      "per_page": "integer"
    }
    ```

### Messaging

#### Send Message

*   **Endpoint:** `POST /api/messages`
*   **Auth:** Required.
*   **Description:** Sends a message to another user.
*   **Request Body:**
    ```json
    {
      "receiver_id": "integer",
      "content": "string"
    }
    ```
*   **Success Response (`201 Created`):** Confirmation and sent message details.
*   **Common Errors:** `400 Bad Request` (missing fields), `401 Unauthorized`, `404 Not Found` (receiver not found).

#### Get Messages

*   **Endpoint:** `GET /api/messages/<other_user_id>`
*   **Auth:** Required.
*   **Description:** Retrieves message history between the authenticated user and another user. Paginated.
*   **Query Parameters:**
    *   `page` (optional, default: 1): Page number.
    *   `per_page` (optional, default: 30): Messages per page.
*   **Success Response (`200 OK`):** Paginated list of messages.
    ```json
    {
      "messages": [ "/* message objects */" ],
      "total": "integer",
      "page": "integer",
      "pages": "integer",
      "per_page": "integer"
    }
    ```
*   **Common Errors:** `401 Unauthorized`, `404 Not Found` (other user not found).

### Posts

#### Create Post

*   **Endpoint:** `POST /api/posts`
*   **Auth:** Required.
*   **Description:** Creates a new post for the authenticated user.
*   **Request Body:**
    ```json
    {
      "content": "string"
    }
    ```
*   **Success Response (`201 Created`):** Confirmation and created post details.
*   **Common Errors:** `400 Bad Request` (missing content), `401 Unauthorized`.

#### Get User Posts

*   **Endpoint:** `GET /api/posts/user/<user_id>`
*   **Auth:** Required.
*   **Description:** Retrieves posts by a specific user. Paginated.
*   **Query Parameters:**
    *   `page` (optional, default: 1): Page number.
    *   `per_page` (optional, default: 10): Posts per page.
*   **Success Response (`200 OK`):** Paginated list of posts including author info.
    ```json
    {
      "posts": [ "/* post objects with author {nom, prenom} */" ],
      "total": "integer",
      "page": "integer",
      "pages": "integer",
      "per_page": "integer"
    }
    ```
*   **Common Errors:** `404 Not Found` (user not found).

#### Update Post

*   **Endpoint:** `PUT /api/posts/<post_id>`
*   **Auth:** Required. Only the author can update their post.
*   **Description:** Updates an existing post.
*   **Request Body:**
    ```json
    {
      "content": "string"
    }
    ```
*   **Success Response (`200 OK`):** Confirmation and updated post details.
*   **Common Errors:** `400 Bad Request` (missing content), `401 Unauthorized`, `403 Forbidden` (not author), `404 Not Found` (post not found).

#### Delete Post

*   **Endpoint:** `DELETE /api/posts/<post_id>`
*   **Auth:** Required. Only the author can delete their post.
*   **Description:** Deletes a post.
*   **Success Response (`200 OK`):** Confirmation message.
*   **Common Errors:** `401 Unauthorized`, `403 Forbidden` (not author), `404 Not Found` (post not found).

## Error Handling

API errors are returned in a standard JSON format:

```json
{
  "error": "A descriptive error message"
}
