from .base import Database
import sqlite3
import logging

class PostManager(Database):
    """Manages post-related database operations."""
    
    def create_post(self, user_id, content, title=None, image=None):
        """Creates a new post."""
        if not title or not content:
            logging.error("Title and content cannot be empty.")
            return None
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                created_at = self.get_current_timestamp()
                cursor.execute(''' 
                    INSERT INTO posts (title, content, image, created_at, user_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (title, content, image, created_at, user_id))
                conn.commit()
                post_id = cursor.lastrowid
                logging.info(f"Post created with ID: {post_id} by user {user_id}")
                return post_id
        except sqlite3.Error as e:
            logging.error(f"Database error creating post for user {user_id}: {e}")
            return None

    def get_posts_by_user(self, user_id, page=1, per_page=10):
        """Retrieves posts by a user with pagination."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) as total FROM posts WHERE user_id = ?', (user_id,))
                total = cursor.fetchone()[0]

                cursor.execute(''' 
                    SELECT p.id, p.title, p.content, p.image, p.created_at, p.user_id,
                           u.first_name, u.last_name, u.photo
                    FROM posts p
                    JOIN users u ON p.user_id = u.id
                    WHERE p.user_id = ?
                    ORDER BY p.created_at DESC
                    LIMIT ? OFFSET ?
                ''', (user_id, per_page, (page - 1) * per_page))
                posts = cursor.fetchall()
                logging.info(f"Retrieved {len(posts)} posts for user {user_id}")
                return posts, total
        except sqlite3.Error as e:
            logging.error(f"Database error getting posts for user {user_id}: {e}")
            return [], 0

    def get_post_by_id(self, post_id):
        """Retrieves a post by ID."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(''' 
                    SELECT p.id, p.title, p.content, p.image, p.created_at, p.user_id,
                           u.first_name, u.last_name, u.photo
                    FROM posts p
                    JOIN users u ON p.user_id = u.id
                    WHERE p.id = ?
                ''', (post_id,))
                post = cursor.fetchone()
                if not post:
                    logging.warning(f"Post {post_id} not found.")
                return post
        except sqlite3.Error as e:
            logging.error(f"Database error getting post by ID {post_id}: {e}")
            return None

    def update_post(self, post_id, title=None, content=None, image=None):
        """Updates a post's title, content, or image."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                # Fetch current post to preserve unchanged fields
                cursor.execute('SELECT title, content, image FROM posts WHERE id = ?', (post_id,))
                current_post = cursor.fetchone()
                if not current_post:
                    logging.warning(f"Post {post_id} not found.")
                    return False
                
                # Use provided values or keep existing ones
                new_title = title if title is not None else current_post[0]
                new_content = content if content is not None else current_post[1]
                new_image = image if image is not None else current_post[2]

                # Ensure title and content are not empty
                if not new_title or not new_content:
                    logging.error("Title and content cannot be empty.")
                    return False

                cursor.execute('''
                    UPDATE posts 
                    SET title = ?, content = ?, image = ?
                    WHERE id = ?
                ''', (new_title, new_content, new_image, post_id))
                conn.commit()
                success = cursor.rowcount > 0
                if success:
                    logging.info(f"Post {post_id} updated successfully.")
                else:
                    logging.warning(f"Post {post_id} not found.")
                return success
        except sqlite3.Error as e:
            logging.error(f"Database error updating post {post_id}: {e}")
            return False

    def delete_post(self, post_id):
        """Deletes a post."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
                conn.commit()
                success = cursor.rowcount > 0
                if success:
                    logging.info(f"Post {post_id} deleted successfully.")
                else:
                    logging.warning(f"Post {post_id} not found.")
                return success
        except sqlite3.Error as e:
            logging.error(f"Database error deleting post {post_id}: {e}")
            return False

    def get_all_posts(self, page=1, per_page=10):
        """Retrieves all posts with pagination."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) as total FROM posts')
                total = cursor.fetchone()[0]
                
                cursor.execute(''' 
                    SELECT p.id, p.title, p.content, p.image, p.created_at, p.user_id,
                           u.first_name, u.last_name, u.photo
                    FROM posts p
                    JOIN users u ON p.user_id = u.id
                    ORDER BY p.created_at DESC
                    LIMIT ? OFFSET ?
                ''', (per_page, (page - 1) * per_page))
                posts = cursor.fetchall()
                logging.info(f"Retrieved {len(posts)} posts. Total: {total}")
                return posts, total
        except sqlite3.Error as e:
            logging.error(f"Database error retrieving all posts: {e}")
            return [], 0