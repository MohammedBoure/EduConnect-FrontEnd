from .base import Database
import sqlite3
import logging

class UserManager(Database):
    """Manages user-related database operations."""

    def create_user(self, first_name, last_name, email, password, department, skills=None, photo=None, role='user'):
        """Creates a new user with hashed password and skills."""
        try:
            hashed_password = self.hash_password(password)
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(''' 
                    INSERT INTO users (first_name, last_name, email, password, department, photo, role)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (first_name, last_name, email, hashed_password, department, photo, role))
                user_id = cursor.lastrowid
                
                # Insert skills
                if skills:
                    skills = skills if isinstance(skills, list) else [s.strip() for s in skills.split(',') if s.strip()]
                    for skill in skills:
                        cursor.execute('INSERT OR IGNORE INTO user_skills (user_id, skill) VALUES (?, ?)', 
                                     (user_id, skill))
                conn.commit()
                logging.info(f"User created successfully with ID: {user_id}")
                return user_id
        except sqlite3.IntegrityError:
            logging.warning(f"Attempted to register existing email: {email}")
            return None
        except sqlite3.Error as e:
            logging.error(f"Database error during user creation for {email}: {e}")
            return None

    def get_user_by_email(self, email):
        """Retrieves a user by email."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Database error getting user by email {email}: {e}")
            return None

    def get_user_by_id(self, user_id):
        """Retrieves a user by ID."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Database error getting user by ID {user_id}: {e}")
            return None

    def update_user(self, user_id, **kwargs):
        """Updates user fields."""
        allowed_fields = {'first_name', 'last_name', 'department', 'photo', 'password', 'email', 'role', 'skills'}
        updates = []
        params = []

        for key, value in kwargs.items():
            if key in allowed_fields and value is not None:
                if key == 'password':
                    updates.append(f"{key} = ?")
                    params.append(self.hash_password(value))
                elif key == 'skills':
                    continue  # Handle skills separately
                else:
                    updates.append(f"{key} = ?")
                    params.append(value)

        if not updates and 'skills' not in kwargs:
            logging.warning(f"Update requested for user {user_id} but no valid fields provided.")
            return False

        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?" if updates else None

        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                if query:
                    cursor.execute(query, params)
                if 'skills' in kwargs and kwargs['skills'] is not None:
                    skills = kwargs['skills'] if isinstance(kwargs['skills'], list) else [s.strip() for s in kwargs['skills'].split(',') if s.strip()]
                    cursor.execute('DELETE FROM user_skills WHERE user_id = ?', (user_id,))
                    for skill in skills:
                        cursor.execute('INSERT OR IGNORE INTO user_skills (user_id, skill) VALUES (?, ?)', 
                                     (user_id, skill))
                conn.commit()
                success = cursor.rowcount > 0 or 'skills' in kwargs
                logging.info(f"User {user_id} updated successfully. Fields: {list(kwargs.keys())}")
                return success
        except sqlite3.Error as e:
            logging.error(f"Database error updating user {user_id}: {e}")
            return False

    def delete_user(self, user_id):
        """Deletes a user and associated data (via CASCADE)."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                conn.commit()
                success = cursor.rowcount > 0
                logging.info(f"User {user_id} deleted successfully.") if success else logging.warning(f"User {user_id} not found.")
                return success
        except sqlite3.Error as e:
            logging.error(f"Database error deleting user {user_id}: {e}")
            return False

    def search_users(self, first_name='', department='', skill='', exclude_user_id=None, page=1, per_page=10):
        """Searches users with pagination."""
        base_query = '''
            SELECT u.id, u.first_name, u.last_name, u.email, u.department, u.photo, u.role,
                   GROUP_CONCAT(us.skill) as skills
            FROM users u
            LEFT JOIN user_skills us ON u.id = us.user_id
        '''
        count_query = "SELECT COUNT(DISTINCT u.id) as total FROM users u LEFT JOIN user_skills us ON u.id = us.user_id"
        conditions = []
        params = []

        if first_name:
            conditions.append("(u.first_name LIKE ? OR u.last_name LIKE ?)")
            params.extend([f'%{first_name}%', f'%{first_name}%'])
        if department:
            conditions.append("u.department LIKE ?")
            params.append(f'%{department}%')
        if skill:
            conditions.append("us.skill LIKE ?")
            params.append(f'%{skill}%')
        if exclude_user_id is not None:
            conditions.append("u.id != ?")
            params.append(exclude_user_id)

        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        group_by = " GROUP BY u.id"

        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(count_query + where_clause, params)
                total = cursor.fetchone()[0]
                
                paginated_query = base_query + where_clause + group_by + " LIMIT ? OFFSET ?"
                params.extend([per_page, (page - 1) * per_page])
                cursor.execute(paginated_query, params)
                users = cursor.fetchall()
                logging.info(f"User search returned {len(users)} results. Total: {total}")
                return users, total
        except sqlite3.Error as e:
            logging.error(f"Database error during user search: {e}")
            return [], 0

    def get_all_users(self, page=1, per_page=10):
        """Retrieves all users with pagination."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) as total FROM users')
                total = cursor.fetchone()[0]
                
                cursor.execute('''
                    SELECT id, first_name, last_name, email, department, photo, role,
                           (SELECT GROUP_CONCAT(skill) FROM user_skills WHERE user_id = u.id) as skills
                    FROM users u
                    ORDER BY first_name, last_name
                    LIMIT ? OFFSET ?
                ''', (per_page, (page - 1) * per_page))
                users = cursor.fetchall()
                logging.info(f"Retrieved {len(users)} users. Total: {total}")
                return users, total
        except sqlite3.Error as e:
            logging.error(f"Database error retrieving all users: {e}")
            return [], 0