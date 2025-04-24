# database/audit.py
from .base import Database
import sqlite3
import logging

class AuditLogManager(Database):
    """Manages audit log entries for administrative actions."""

    def log_action(self, admin_id, action, resource_type, resource_id, details=None):
        """Logs an administrative action."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                created_at = self.get_current_timestamp()
                cursor.execute(''' 
                    INSERT INTO audit_logs (action, resource_type, resource_id, admin_id, details, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (action, resource_type, resource_id, admin_id, details, created_at))
                conn.commit()
                log_id = cursor.lastrowid
                logging.info(f"Audit log created with ID: {log_id} for action {action} on {resource_type} {resource_id}")
                return log_id
        except sqlite3.Error as e:
            logging.error(f"Database error logging action {action} for {resource_type} {resource_id}: {e}")
            return None

    def get_audit_logs(self, page=1, per_page=50):
        """Retrieves audit logs with pagination."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Get the total count of audit logs
                cursor.execute('SELECT COUNT(*) as total FROM audit_logs')
                total = cursor.fetchone()['total']
                
                # Fetch the paginated audit logs
                cursor.execute('''
                    SELECT id, action, resource_type, resource_id, admin_id, details, created_at
                    FROM audit_logs
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                ''', (per_page, (page - 1) * per_page))
                logs = cursor.fetchall()
                
                logging.info(f"Retrieved {len(logs)} audit logs. Total: {total}")
                return logs, total
        except sqlite3.Error as e:
            logging.error(f"Database error retrieving audit logs: {e}")
            return [], 0
