import sqlite3
import logging
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Database:
    """Base class for managing SQLite database connections and schema initialization."""
    
    DB_FILE = 'database/student_directory.db'

    def __init__(self):
        """Initialize the database and create schema."""
        self.init_db()

    def get_db_connection(self):
        """Establishes a new SQLite connection with row factory and foreign key support."""
        try:
            conn = sqlite3.connect(self.DB_FILE, timeout=10)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            logging.error(f"Database connection error: {e}")
            raise

    def init_db(self):
        """Initializes the database schema with tables and indexes."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                logging.info("Initializing database schema...")

                # Create users table with role
                cursor.execute(''' 
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        department TEXT NOT NULL,
                        photo TEXT,
                        role TEXT NOT NULL DEFAULT 'user' CHECK(role IN ('user', 'admin'))
                    )
                ''')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
                logging.info("Table 'users' checked/created.")

                # Create user_skills table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_skills (
                        user_id INTEGER NOT NULL,
                        skill TEXT NOT NULL,
                        PRIMARY KEY (user_id, skill),
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                ''')
                logging.info("Table 'user_skills' checked/created.")

                # Create posts table with title and image
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        image TEXT,
                        created_at TEXT NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                ''')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id)')
                logging.info("Table 'posts' checked/created.")

                # Create messages table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        sender_id INTEGER NOT NULL,
                        receiver_id INTEGER NOT NULL,
                        FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                ''')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_sender_id ON messages(sender_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_receiver_id ON messages(receiver_id)')
                logging.info("Table 'messages' checked/created.")

                # Create comments table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS comments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        user_id INTEGER NOT NULL,
                        post_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
                    )
                ''')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments(user_id)')
                logging.info("Table 'comments' checked/created.")

                # Create audit_logs table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS audit_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        action TEXT NOT NULL,
                        resource_type TEXT NOT NULL,
                        resource_id INTEGER NOT NULL,
                        admin_id INTEGER,
                        details TEXT,
                        created_at TEXT NOT NULL,
                        FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE SET NULL
                    )
                ''')
                logging.info("Table 'audit_logs' checked/created.")

                conn.commit()
                logging.info("Database schema initialization complete.")
        except sqlite3.Error as e:
            logging.error(f"Database initialization failed: {e}")
            raise

    @staticmethod
    def hash_password(password):
        """Hashes a password using werkzeug.security."""
        return generate_password_hash(password)

    @staticmethod
    def check_password(pwhash, password):
        """Checks if a password matches the stored hash."""
        return check_password_hash(pwhash, password)

    @staticmethod
    def get_current_timestamp():
        """Returns the current UTC timestamp in ISO8601 format."""
        return datetime.utcnow().isoformat() + "Z"