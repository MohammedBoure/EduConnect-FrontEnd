# database/message.py
from .base import Database
import sqlite3
import logging

class MessageManager(Database):
    """Manages message-related database operations."""

    def send_message(self, sender_id, receiver_id, content):
        """Sends a message from one user to another."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                created_at = self.get_current_timestamp()
                cursor.execute(''' 
                    INSERT INTO messages (content, created_at, sender_id, receiver_id)
                    VALUES (?, ?, ?, ?)
                ''', (content, created_at, sender_id, receiver_id))
                conn.commit()
                message_id = cursor.lastrowid
                logging.info(f"Message sent with ID: {message_id} from {sender_id} to {receiver_id}")
                return message_id
        except sqlite3.Error as e:
            logging.error(f"Database error sending message from {sender_id} to {receiver_id}: {e}")
            return None

    def get_messages_between_users(self, user1_id, user2_id, page=1, per_page=30):
        """Retrieves messages between two users with pagination."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT COUNT(*) as total FROM messages
                    WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
                ''', (user1_id, user2_id, user2_id, user1_id))
                total = cursor.fetchone()[0]

                cursor.execute('''
                    SELECT * FROM messages
                    WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                ''', (user1_id, user2_id, user2_id, user1_id, per_page, (page - 1) * per_page))
                messages = cursor.fetchall()
                logging.info(f"Retrieved {len(messages)} messages between {user1_id} and {user2_id}")
                return messages, total
        except sqlite3.Error as e:
            logging.error(f"Database error getting messages between {user1_id} and {user2_id}: {e}")
            return [], 0

    def get_message_by_id(self, message_id):
        """Retrieves a message by ID."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM messages WHERE id = ?', (message_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Database error getting message by ID {message_id}: {e}")
            return None

    def delete_message(self, message_id):
        """Deletes a message."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM messages WHERE id = ?', (message_id,))
                conn.commit()
                success = cursor.rowcount > 0
                if success:
                    logging.info(f"Message {message_id} deleted successfully.")
                else:
                    logging.warning(f"Message {message_id} not found.")
                return success
        except sqlite3.Error as e:
            logging.error(f"Database error deleting message {message_id}: {e}")
            return False

    def get_all_messages(self, page=1, per_page=30):
        """Retrieves all messages with pagination."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) as total FROM messages')
                total = cursor.fetchone()[0]

                cursor.execute('''
                    SELECT id, content, created_at, sender_id, receiver_id
                    FROM messages
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                ''', (per_page, (page - 1) * per_page))
                messages = cursor.fetchall()
                logging.info(f"Retrieved {len(messages)} messages. Total: {total}")
                return messages, total
        except sqlite3.Error as e:
            logging.error(f"Database error retrieving all messages: {e}")
            return [], 0
