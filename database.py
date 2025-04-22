import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import logging # Import logging
from werkzeug.security import check_password_hash as werkzeug_check_password_hash

# --- Configuration ---
DB_FILE = 'student_directory.db'
# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Database Connection ---

def get_db_connection():
    """Establishes and returns a new SQLite connection to the database file.

    Configures the connection to return rows as dictionary-like objects
    (sqlite3.Row) for easier column access by name.
    """
    try:
        conn = sqlite3.connect(DB_FILE, timeout=10) # Added timeout
        conn.row_factory = sqlite3.Row
        # Enable foreign key support (good practice for SQLite)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        raise # Re-raise the exception after logging

def init_db():
    """Initializes the database.

    Creates the necessary tables ('utilisateurs', 'posts', 'messages', 'comments')
    if they don't already exist. Includes foreign key constraints with
    cascading deletes where appropriate.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            logging.info("Initializing database schema...")

            # Create utilisateurs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS utilisateurs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    mot_de_passe TEXT NOT NULL,
                    filiere TEXT NOT NULL,
                    competences TEXT, -- Allow NULL or empty string
                    photo TEXT
                )
            ''')
            logging.info("Table 'utilisateurs' checked/created.")

            # Create posts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL, -- Store as ISO8601 string
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
                )
            ''')
            logging.info("Table 'posts' checked/created.")

            # Create messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL, -- Store as ISO8601 string
                    sender_id INTEGER NOT NULL,
                    receiver_id INTEGER NOT NULL,
                    FOREIGN KEY (sender_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
                    FOREIGN KEY (receiver_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
                )
            ''')
            logging.info("Table 'messages' checked/created.")

            # --- NEW: Create comments table ---
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL, -- Store as ISO8601 string
                    user_id INTEGER NOT NULL,
                    post_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
                    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
                )
            ''')
            logging.info("Table 'comments' checked/created.")
            # --- END NEW ---

            conn.commit()
            logging.info("Database schema initialization complete.")
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during DB init: {e}")


# --- Password Hashing ---

# Note: check_password_hash is imported but not defined here.
# It's assumed to be available where needed (e.g., in the Flask app).
# Let's add it here for completeness if this module is meant to be self-contained.
def check_password_hash(pwhash, password):
    """Checks if the provided password matches the stored hash."""
    return werkzeug_check_password_hash(pwhash, password)


# --- User Operations ---

def create_user(nom, prenom, email, mot_de_passe, filiere, competences, photo=None):
    """Creates a new user in the database with a hashed password.

    Args:
        nom (str): User's last name.
        prenom (str): User's first name.
        email (str): User's unique email address.
        mot_de_passe (str): User's plaintext password (will be hashed).
        filiere (str): User's field of study/department.
        competences (list or str): User's skills (converted to comma-separated string).
        photo (str, optional): URL or path to the user's photo. Defaults to None.

    Returns:
        int: The ID of the newly created user, or None if the email already
             exists or another error occurred.
    """
    try:
        # Ensure competences is stored as a string
        competences_str = ','.join(filter(None, competences)) if isinstance(competences, list) else str(competences or '')
        hashed_password = generate_password_hash(mot_de_passe)
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, filiere, competences, photo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nom, prenom, email, hashed_password, filiere, competences_str, photo))
            conn.commit()
            user_id = cursor.lastrowid
            logging.info(f"User created successfully with ID: {user_id}")
            return user_id
    except sqlite3.IntegrityError:
        logging.warning(f"Attempted to register existing email: {email}")
        return None  # Email already exists
    except sqlite3.Error as e:
        logging.error(f"Database error during user creation for {email}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error during user creation: {e}")
        return None

def get_user_by_email(email):
    """Retrieves a user's details by their email address.

    Args:
        email (str): The email address to search for.

    Returns:
        sqlite3.Row: A dictionary-like object containing the user's data,
                     or None if no user is found with that email.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM utilisateurs WHERE email = ?', (email,))
            user = cursor.fetchone()
            # logging.info(f"User lookup by email '{email}' {'found' if user else 'not found'}.")
            return user
    except sqlite3.Error as e:
        logging.error(f"Database error getting user by email {email}: {e}")
        return None

def get_user_by_id(user_id):
    """Retrieves a user's details by their unique ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        sqlite3.Row: A dictionary-like object containing the user's data,
                     or None if no user is found with that ID.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM utilisateurs WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            # logging.info(f"User lookup by ID '{user_id}' {'found' if user else 'not found'}.")
            return user
    except sqlite3.Error as e:
        logging.error(f"Database error getting user by ID {user_id}: {e}")
        return None

def update_user(user_id, **kwargs):
    """Updates specified fields for a given user ID.

    Accepts keyword arguments for the fields to update (e.g., nom, prenom,
    filiere, competences, photo). Ignores fields not provided.

    Args:
        user_id (int): The ID of the user to update.
        **kwargs: Keyword arguments mapping column names to new values.
                  'competences' can be a list or string.

    Returns:
        bool: True if the update was successful (at least one row affected),
              False otherwise or if an error occurred.
    """
    allowed_fields = {'nom', 'prenom', 'filiere', 'competences', 'photo', 'mot_de_passe'}
    updates = []
    params = []

    for key, value in kwargs.items():
        if key in allowed_fields and value is not None:
            if key == 'competences':
                # Ensure competences is stored as a string
                value_str = ','.join(filter(None, value)) if isinstance(value, list) else str(value or '')
                updates.append(f"{key} = ?")
                params.append(value_str)
            elif key == 'mot_de_passe':
                # Hash password if updating it
                updates.append(f"{key} = ?")
                params.append(generate_password_hash(value))
            else:
                updates.append(f"{key} = ?")
                params.append(value)

    if not updates:
        logging.warning(f"Update requested for user {user_id} but no valid fields provided.")
        return False  # Nothing to update

    params.append(user_id)
    query = f"UPDATE utilisateurs SET {', '.join(updates)} WHERE id = ?"

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            success = cursor.rowcount > 0
            if success:
                logging.info(f"User {user_id} updated successfully. Fields: {list(kwargs.keys())}")
            else:
                logging.warning(f"User {user_id} update attempted, but no rows affected (maybe user not found?).")
            return success
    except sqlite3.Error as e:
        logging.error(f"Database error updating user {user_id}: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error updating user {user_id}: {e}")
        return False


def delete_user(user_id):
    """Deletes a user and their associated data (posts, messages, comments)
    due to CASCADE constraints.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        bool: True if the user was successfully deleted (one row affected),
              False otherwise or if an error occurred.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Foreign key constraints with ON DELETE CASCADE handle related data
            cursor.execute('DELETE FROM utilisateurs WHERE id = ?', (user_id,))
            conn.commit()
            success = cursor.rowcount > 0
            if success:
                 logging.info(f"User {user_id} and associated data deleted successfully.")
            else:
                 logging.warning(f"Attempted to delete user {user_id}, but user not found.")
            return success
    except sqlite3.Error as e:
        logging.error(f"Database error deleting user {user_id}: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error deleting user {user_id}: {e}")
        return False

def search_users(nom='', filiere='', competence='', exclude_user_id=None, page=1, per_page=10):
    """Searches for users based on criteria with pagination.

    Filters users by name (nom or prenom), filiere, and competence using
    LIKE matching. Can exclude a specific user ID (e.g., the logged-in user).

    Args:
        nom (str, optional): Search term for first or last name. Defaults to ''.
        filiere (str, optional): Search term for filiere. Defaults to ''.
        competence (str, optional): Search term for competences. Defaults to ''.
        exclude_user_id (int, optional): User ID to exclude from results. Defaults to None.
        page (int, optional): The page number to retrieve (1-based). Defaults to 1.
        per_page (int, optional): Number of results per page. Defaults to 10.

    Returns:
        tuple: A tuple containing:
               - list: A list of user rows (sqlite3.Row objects) matching the criteria.
               - int: The total number of users matching the criteria (before pagination).
               Returns ([], 0) if an error occurs.
    """
    base_query = "SELECT id, nom, prenom, email, filiere, competences, photo FROM utilisateurs" # Select specific columns
    count_query = "SELECT COUNT(*) as total FROM utilisateurs"
    conditions = []
    params = []

    if nom:
        conditions.append("(nom LIKE ? OR prenom LIKE ?)")
        params.extend([f'%{nom}%', f'%{nom}%'])
    if filiere:
        conditions.append("filiere LIKE ?")
        params.append(f'%{filiere}%')
    if competence:
        # Assumes competences are comma-separated, search for the term within the string
        conditions.append("competences LIKE ?")
        params.append(f'%{competence}%')
    if exclude_user_id is not None:
        conditions.append("id != ?")
        params.append(exclude_user_id)

    where_clause = ""
    if conditions:
        where_clause = " WHERE " + " AND ".join(conditions)

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Count total matching users
            cursor.execute(count_query + where_clause, params)
            total_row = cursor.fetchone()
            total = total_row['total'] if total_row else 0

            # Fetch paginated results
            paginated_query = base_query + where_clause + " ORDER BY nom, prenom LIMIT ? OFFSET ?"
            offset = (page - 1) * per_page
            params.extend([per_page, offset])
            cursor.execute(paginated_query, params)
            users = cursor.fetchall()

            # logging.info(f"User search yielded {len(users)} results (page {page}/{ (total + per_page - 1) // per_page if per_page > 0 else 1 }). Total matches: {total}")
            return users, total
    except sqlite3.Error as e:
        logging.error(f"Database error during user search: {e}")
        return [], 0
    except Exception as e:
        logging.error(f"Unexpected error during user search: {e}")
        return [], 0


# --- Post Operations ---

def create_post(user_id, content):
    """Creates a new post associated with a user.

    Args:
        user_id (int): The ID of the user creating the post.
        content (str): The text content of the post.

    Returns:
        int: The ID of the newly created post, or None if an error occurred.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            created_at = datetime.utcnow().isoformat() + "Z" # Add Z for UTC indication
            cursor.execute('''
                INSERT INTO posts (content, created_at, user_id)
                VALUES (?, ?, ?)
            ''', (content, created_at, user_id))
            conn.commit()
            post_id = cursor.lastrowid
            logging.info(f"Post created successfully with ID: {post_id} by user {user_id}")
            return post_id
    except sqlite3.Error as e:
        logging.error(f"Database error creating post for user {user_id}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error creating post: {e}")
        return None

def get_posts_by_user(user_id, page=1, per_page=10):
    """Retrieves posts created by a specific user, with pagination.

    Joins with the 'utilisateurs' table to include author's name (nom, prenom)
    and photo in the results. Orders posts by creation date, newest first.

    Args:
        user_id (int): The ID of the user whose posts to retrieve.
        page (int, optional): Page number (1-based). Defaults to 1.
        per_page (int, optional): Posts per page. Defaults to 10.

    Returns:
        tuple: A tuple containing:
               - list: A list of post rows (sqlite3.Row including author details).
               - int: The total number of posts by this user.
               Returns ([], 0) if an error occurs.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Count total for pagination
            cursor.execute('SELECT COUNT(*) as total FROM posts WHERE user_id = ?', (user_id,))
            total_row = cursor.fetchone()
            total = total_row['total'] if total_row else 0

            # Paginated query with JOIN
            offset = (page - 1) * per_page
            cursor.execute('''
                SELECT p.id, p.content, p.created_at, p.user_id,
                       u.nom, u.prenom, u.photo
                FROM posts p
                JOIN utilisateurs u ON p.user_id = u.id
                WHERE p.user_id = ?
                ORDER BY p.created_at DESC
                LIMIT ? OFFSET ?
            ''', (user_id, per_page, offset))
            posts = cursor.fetchall()
            # logging.info(f"Retrieved {len(posts)} posts for user {user_id} (page {page}). Total: {total}")
            return posts, total
    except sqlite3.Error as e:
        logging.error(f"Database error getting posts for user {user_id}: {e}")
        return [], 0
    except Exception as e:
        logging.error(f"Unexpected error getting posts for user {user_id}: {e}")
        return [], 0

def update_post(post_id, content):
    """Updates the content of an existing post.

    Args:
        post_id (int): The ID of the post to update.
        content (str): The new content for the post.

    Returns:
        bool: True if the update was successful (one row affected), False otherwise.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE posts SET content = ? WHERE id = ?', (content, post_id))
            conn.commit()
            success = cursor.rowcount > 0
            if success:
                logging.info(f"Post {post_id} updated successfully.")
            else:
                logging.warning(f"Update post {post_id} attempted, but no rows affected (maybe post not found?).")
            return success
    except sqlite3.Error as e:
        logging.error(f"Database error updating post {post_id}: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error updating post {post_id}: {e}")
        return False

def delete_post(post_id):
    """Deletes a post and its associated comments (due to CASCADE constraint).

    Args:
        post_id (int): The ID of the post to delete.

    Returns:
        bool: True if the post was successfully deleted (one row affected), False otherwise.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Comments associated with this post will be deleted due to ON DELETE CASCADE
            cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
            conn.commit()
            success = cursor.rowcount > 0
            if success:
                logging.info(f"Post {post_id} and associated comments deleted successfully.")
            else:
                 logging.warning(f"Attempted to delete post {post_id}, but post not found.")
            return success
    except sqlite3.Error as e:
        logging.error(f"Database error deleting post {post_id}: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error deleting post {post_id}: {e}")
        return False

def get_post_by_id(post_id):
    """Retrieves a single post by its ID, including author details.

    Args:
        post_id (int): The ID of the post to retrieve.

    Returns:
        sqlite3.Row: A dictionary-like object containing the post data and
                     author details (nom, prenom, photo), or None if not found.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Join with users to get author details
            cursor.execute('''
                SELECT p.id, p.content, p.created_at, p.user_id,
                       u.nom, u.prenom, u.photo
                FROM posts p
                JOIN utilisateurs u ON p.user_id = u.id
                WHERE p.id = ?
            ''', (post_id,))
            post = cursor.fetchone()
            # logging.info(f"Post lookup by ID '{post_id}' {'found' if post else 'not found'}.")
            return post
    except sqlite3.Error as e:
        logging.error(f"Database error getting post by ID {post_id}: {e}")
        return None

# --- Message Operations ---

def send_message(sender_id, receiver_id, content):
    """Sends a private message from one user to another.

    Args:
        sender_id (int): The ID of the user sending the message.
        receiver_id (int): The ID of the user receiving the message.
        content (str): The text content of the message.

    Returns:
        int: The ID of the newly created message, or None if an error occurred.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            created_at = datetime.utcnow().isoformat() + "Z" # Add Z for UTC indication
            cursor.execute('''
                INSERT INTO messages (content, created_at, sender_id, receiver_id)
                VALUES (?, ?, ?, ?)
            ''', (content, created_at, sender_id, receiver_id))
            conn.commit()
            message_id = cursor.lastrowid
            logging.info(f"Message sent successfully with ID: {message_id} from {sender_id} to {receiver_id}")
            return message_id
    except sqlite3.Error as e:
        logging.error(f"Database error sending message from {sender_id} to {receiver_id}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error sending message: {e}")
        return None

def get_messages_between_users(user1_id, user2_id, page=1, per_page=30):
    """Retrieves the conversation history between two users, paginated.

    Fetches messages where either user is the sender and the other is the
    receiver. Orders messages by creation date, newest first (suitable for
    typical chat display where newest is at the bottom, requiring reversal later).

    Args:
        user1_id (int): ID of the first user.
        user2_id (int): ID of the second user.
        page (int, optional): Page number (1-based). Defaults to 1.
        per_page (int, optional): Messages per page. Defaults to 30.

    Returns:
        tuple: A tuple containing:
               - list: A list of message rows (sqlite3.Row).
               - int: The total number of messages in the conversation.
               Returns ([], 0) if an error occurs.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Count total for pagination
            cursor.execute('''
                SELECT COUNT(*) as total FROM messages
                WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
            ''', (user1_id, user2_id, user2_id, user1_id))
            total_row = cursor.fetchone()
            total = total_row['total'] if total_row else 0

            # Paginated query
            offset = (page - 1) * per_page
            cursor.execute('''
                SELECT * FROM messages
                WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (user1_id, user2_id, user2_id, user1_id, per_page, offset))
            messages = cursor.fetchall()
            # logging.info(f"Retrieved {len(messages)} messages between {user1_id} and {user2_id} (page {page}). Total: {total}")
            return messages, total
    except sqlite3.Error as e:
        logging.error(f"Database error getting messages between {user1_id} and {user2_id}: {e}")
        return [], 0
    except Exception as e:
        logging.error(f"Unexpected error getting messages between {user1_id} and {user2_id}: {e}")
        return [], 0

def get_message_by_id(message_id):
    """Retrieves a single message by its ID.

    Args:
        message_id (int): The ID of the message to retrieve.

    Returns:
        sqlite3.Row: Dictionary-like object with message data, or None if not found.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM messages WHERE id = ?', (message_id,))
            message = cursor.fetchone()
            return message
    except sqlite3.Error as e:
        logging.error(f"Database error getting message by ID {message_id}: {e}")
        return None


# --- Comment Operations ---

def create_comment(post_id, user_id, content):
    """Creates a new comment on a specific post.

    Args:
        post_id (int): The ID of the post being commented on.
        user_id (int): The ID of the user making the comment.
        content (str): The text content of the comment.

    Returns:
        int: The ID of the newly created comment, or None if an error occurred.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            created_at = datetime.utcnow().isoformat() + "Z" # Add Z for UTC indication
            cursor.execute('''
                INSERT INTO comments (post_id, user_id, content, created_at)
                VALUES (?, ?, ?, ?)
            ''', (post_id, user_id, content, created_at))
            conn.commit()
            comment_id = cursor.lastrowid
            logging.info(f"Comment created successfully with ID: {comment_id} on post {post_id} by user {user_id}")
            return comment_id
    except sqlite3.IntegrityError as e:
         # This might happen if the post_id or user_id doesn't exist, due to foreign key constraints
         logging.error(f"Integrity error creating comment on post {post_id} by user {user_id}: {e}. Check if post/user exist.")
         return None
    except sqlite3.Error as e:
        logging.error(f"Database error creating comment on post {post_id} by user {user_id}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error creating comment: {e}")
        return None

def get_comments_by_post(post_id, page=1, per_page=20):
    """Retrieves comments for a specific post, with pagination and author details.

    Joins with the 'utilisateurs' table to include the comment author's details
    (nom, prenom, photo). Orders comments chronologically (oldest first).

    Args:
        post_id (int): The ID of the post whose comments to retrieve.
        page (int, optional): Page number (1-based). Defaults to 1.
        per_page (int, optional): Comments per page. Defaults to 20.

    Returns:
        tuple: A tuple containing:
               - list: A list of comment rows (sqlite3.Row including author details).
               - int: The total number of comments on this post.
               Returns ([], 0) if an error occurs.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Count total comments for the post
            cursor.execute('SELECT COUNT(*) as total FROM comments WHERE post_id = ?', (post_id,))
            total_row = cursor.fetchone()
            total = total_row['total'] if total_row else 0

            # Paginated query with JOIN to get author details
            offset = (page - 1) * per_page
            cursor.execute('''
                SELECT c.id, c.content, c.created_at, c.user_id, c.post_id,
                       u.nom, u.prenom, u.photo
                FROM comments c
                JOIN utilisateurs u ON c.user_id = u.id
                WHERE c.post_id = ?
                ORDER BY c.created_at ASC  -- Chronological order
                LIMIT ? OFFSET ?
            ''', (post_id, per_page, offset))
            comments = cursor.fetchall()
            # logging.info(f"Retrieved {len(comments)} comments for post {post_id} (page {page}). Total: {total}")
            return comments, total
    except sqlite3.Error as e:
        logging.error(f"Database error getting comments for post {post_id}: {e}")
        return [], 0
    except Exception as e:
        logging.error(f"Unexpected error getting comments for post {post_id}: {e}")
        return [], 0

def get_comment_by_id(comment_id):
    """Retrieves a single comment by its ID, including author details.

    Args:
        comment_id (int): The ID of the comment to retrieve.

    Returns:
        sqlite3.Row: A dictionary-like object containing the comment data and
                     author details (nom, prenom, photo), or None if not found.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.id, c.content, c.created_at, c.user_id, c.post_id,
                       u.nom, u.prenom, u.photo
                FROM comments c
                JOIN utilisateurs u ON c.user_id = u.id
                WHERE c.id = ?
            ''', (comment_id,))
            comment = cursor.fetchone()
            # logging.info(f"Comment lookup by ID '{comment_id}' {'found' if comment else 'not found'}.")
            return comment
    except sqlite3.Error as e:
        logging.error(f"Database error getting comment by ID {comment_id}: {e}")
        return None

def update_comment(comment_id, content):
    """Updates the content of an existing comment.

    Args:
        comment_id (int): The ID of the comment to update.
        content (str): The new text content for the comment.

    Returns:
        bool: True if the update was successful (one row affected), False otherwise.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE comments SET content = ? WHERE id = ?', (content, comment_id))
            conn.commit()
            success = cursor.rowcount > 0
            if success:
                logging.info(f"Comment {comment_id} updated successfully.")
            else:
                logging.warning(f"Update comment {comment_id} attempted, but no rows affected (maybe comment not found?).")
            return success
    except sqlite3.Error as e:
        logging.error(f"Database error updating comment {comment_id}: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error updating comment {comment_id}: {e}")
        return False

def delete_comment(comment_id):
    """Deletes a specific comment.

    Args:
        comment_id (int): The ID of the comment to delete.

    Returns:
        bool: True if the comment was successfully deleted (one row affected), False otherwise.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
            conn.commit()
            success = cursor.rowcount > 0
            if success:
                logging.info(f"Comment {comment_id} deleted successfully.")
            else:
                logging.warning(f"Attempted to delete comment {comment_id}, but comment not found.")
            return success
    except sqlite3.Error as e:
        logging.error(f"Database error deleting comment {comment_id}: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error deleting comment {comment_id}: {e}")
        return False

# --- Main Execution (for initialization) ---

if __name__ == "__main__":
    print("Running database initialization...")
    init_db()
    print("Database initialization process finished.")
    # Example usage (optional, for testing)
    """conn = get_db_connection()
    if conn:
        print("Database connection successful.")
        conn.close()
    else:
        print("Database connection failed.")"""