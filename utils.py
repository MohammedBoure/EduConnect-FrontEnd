from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from functools import wraps
from flask import jsonify
import database

def safe_get_jwt_identity_as_int():
    try:
        identity_str = get_jwt_identity()
        return int(identity_str)
    except Exception as e:
        print(f"Error getting or converting JWT identity: {e}")
        return None

def get_optional_jwt_identity_as_int():
    try:
        verify_jwt_in_request(optional=True)
        return safe_get_jwt_identity_as_int()
    except Exception as e:
        print(f"Optional JWT check failed or no token present: {e}")
        return None

def require_admin_role(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = safe_get_jwt_identity_as_int()
        if user_id is None:
            return jsonify({'error': 'Invalid token identity'}), 401
        user = database.UserManager.get_user_by_id(user_id)
        if not user or user['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function