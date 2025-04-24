from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from database import UserManager
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)
user_manager = UserManager()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['first_name', 'last_name', 'email', 'password', 'department', 'skills']

    if not data or not all(field in data and data[field] for field in required_fields):
        return jsonify({'error': 'All fields are required and cannot be empty'}), 400

    # Check password length
    if len(data['password']) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long'}), 400

    if user_manager.get_user_by_email(data['email']):
        return jsonify({'error': 'Email already exists'}), 409

    user_id = user_manager.create_user(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'],
        department=data['department'],
        skills=data['skills'],
        photo=data.get('photo')
    )
    
    print(user_id)
    if user_id:
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user_id,
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email']
            }
        }), 201

    return jsonify({'error': 'Database error during registration'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = user_manager.get_user_by_email(data['email'])
    if user and check_password_hash(user['password'], data['password']):
        access_token = create_access_token(identity=str(user['id']))
        return jsonify({
            'access_token': access_token,
            'user_id': user['id']
        }), 200
    return jsonify({'error': 'Invalid email or password'}), 401