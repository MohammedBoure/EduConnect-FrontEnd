# database/comment.py
from .base import Database
import sqlite3
import logging

class CommentManager(Database):
    """Manages comment-related database operations."""

    def create_comment(self, post_id, user_id, content):
        """Creates a new comment on a post."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()

                # Check if the post_id exists
                cursor.execute('SELECT 1 FROM posts WHERE id = ?', (post_id,))
                if cursor.fetchone() is None:
                    logging.error(f"Post {post_id} does not exist.")
                    return None

                # Check if the user_id exists
                cursor.execute('SELECT 1 FROM utilisateurs WHERE id = ?', (user_id,))
                if cursor.fetchone() is None:
                    logging.error(f"User {user_id} does not exist.")
                    return None

                created_at = self.get_current_timestamp()
                cursor.execute(''' 
                    INSERT INTO comments (post_id, user_id, content, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (post_id, user_id, content, created_at))
                conn.commit()
                comment_id = cursor.lastrowid
                logging.info(f"Comment created with ID: {comment_id} on post {post_id} by user {user_id}")
                return comment_id
        except sqlite3.IntegrityError:
            logging.error(f"Integrity error creating comment on post {post_id} by user {user_id}: Invalid post/user ID")
            return None
        except sqlite3.Error as e:
            logging.error(f"Database error creating comment on post {post_id}: {e}")
            return None


    def get_comments_by_post(self, post_id, page=1, per_page=20):
        """Retrieves comments for a post with pagination."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) as total FROM comments WHERE post_id = ?', (post_id,))
                total = cursor.fetchone()['total']
                
                cursor.execute('''
                    SELECT c.id, c.content, c.created_at, c.user_id, c.post_id,
                           u.nom, u.prenom, u.photo
                    FROM comments c
                    JOIN utilisateurs u ON c.user_id = u.id
                    WHERE c.post_id = ?
                    ORDER BY c.created_at ASC
                    LIMIT ? OFFSET ?
                ''', (post_id, per_page, (page - 1) * per_page))
                comments = cursor.fetchall()
                logging.info(f"Retrieved {len(comments)} comments for post {post_id}")
                return comments, total
        except sqlite3.Error as e:
            logging.error(f"Database error getting comments for post {post_id}: {e}")
            return [], 0

    def get_comment_by_id(self, comment_id):
        """Retrieves a comment by ID."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT c.id, c.content, c.created_at, c.user_id, c.post_id,
                           u.nom, u.prenom, u.photo
                    FROM comments c
                    JOIN utilisateurs u ON c.user_id = u.id
                    WHERE c.id = ?
                ''', (comment_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Database error getting comment by ID {comment_id}: {e}")
            return None

    def update_comment(self, comment_id, content):
        """Updates a comment's content."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE comments SET content = ? WHERE id = ?', (content, comment_id))
                conn.commit()
                success = cursor.rowcount > 0
                logging.info(f"Comment {comment_id} updated successfully.") if success else logging.warning(f"Comment {comment_id} not found.")
                return success
        except sqlite3.Error as e:
            logging.error(f"Database error updating comment {comment_id}: {e}")
            return False

    def delete_comment(self, comment_id):
        """Deletes a comment."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
                conn.commit()
                success = cursor.rowcount > 0
                logging.info(f"Comment {comment_id} deleted successfully.") if success else logging.warning(f"Comment {comment_id} not found.")
                return success
        except sqlite3.Error as e:
            logging.error(f"Database error deleting comment {comment_id}: {e}")
            return False

    def get_all_comments(self, page=1, per_page=20):
        """Retrieves all comments with pagination."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) as total FROM comments')
                total = cursor.fetchone()['total']
                
                cursor.execute('''
                    SELECT c.id, c.content, c.created_at, c.user_id, c.post_id,
                           u.nom, u.prenom, u.photo
                    FROM comments c
                    JOIN utilisateurs u ON c.user_id = u.id
                    ORDER BY c.created_at DESC
                    LIMIT ? OFFSET ?
                ''', (per_page, (page - 1) * per_page))
                comments = cursor.fetchall()
                logging.info(f"Retrieved {len(comments)} comments. Total: {total}")
                return comments, total
        except sqlite3.Error as e:
            logging.error(f"Database error retrieving all comments: {e}")
            return [], 0
