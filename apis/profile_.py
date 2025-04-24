from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils import safe_get_jwt_identity_as_int

profile_bp = Blueprint('profile', __name__)
from database import UserManager,AuditLogManager

user_manager = UserManager()
audit_log_manager = AuditLogManager()

def log_admin_action(admin_id, action, resource_type, resource_id, details=None):
    """Log administrative actions for auditing purposes."""
    audit_log_manager.log_action(admin_id, action, resource_type, resource_id, details)


@profile_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    """Retrieve details of a specific user by ID."""
    user = user_manager.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    skills = user_manager.search_users(skill='', exclude_user_id=None, page=1, per_page=1)[0]
    skills_list = [skill.strip() for skill in skills[0]['skills'].split(',') if skill.strip()] if skills[0]['skills'] else []
    
    return jsonify({
        'id': user['id'],
        'last_name': user['last_name'],
        'first_name': user['first_name'],
        'email': user['email'],
        'department': user['department'],
        'skills': skills_list,
        'photo': user['photo'],
        'role': user['role']
    }), 200

@profile_bp.route('/profile/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_profile(user_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
        return jsonify({'error': 'Invalid token identity'}), 401
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized: You can only update your own profile'}), 403

    """Update a user's details, including their role."""
    user = user_manager.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No update data provided'}), 400

    skills_data = data.get('skills')
    skills = None
    if skills_data is not None:
        skills = skills_data if isinstance(skills_data, list) else [skill.strip() for skill in skills_data.split(',') if skill.strip()]

    update_payload = {}
    if data.get('last_name') is not None: update_payload['last_name'] = data['last_name']
    if data.get('first_name') is not None: update_payload['first_name'] = data['first_name']
    if data.get('department') is not None: update_payload['department'] = data['department']
    if skills is not None: update_payload['skills'] = skills
    if data.get('photo') is not None: update_payload['photo'] = data['photo']
    if data.get('role') in ['user', 'admin']: update_payload['role'] = data['role']
    if data.get('email') is not None: update_payload['email'] = data['email']
    if data.get('password') is not None: update_payload['password'] = data['password']

    if not update_payload:
        return jsonify({'error': 'No valid fields provided for update'}), 400

    success = user_manager.update_user(user_id, **update_payload)
    if success:
        log_admin_action(0, 'update_user', 'user', user_id, f"Updated fields: {list(update_payload.keys())}")
        updated_user = user_manager.get_user_by_id(user_id)
        skills = user_manager.search_users(skill='', exclude_user_id=None, page=1, per_page=1)[0]
        skills_list = [skill.strip() for skill in skills[0]['skills'].split(',') if skill.strip()] if skills[0]['skills'] else []
        return jsonify({
            'message': 'User updated successfully',
            'user': {
                'id': updated_user['id'],
                'last_name': updated_user['last_name'],
                'first_name': updated_user['first_name'],
                'email': updated_user['email'],
                'department': updated_user['department'],
                'skills': skills_list,
                'photo': updated_user['photo'],
                'role': updated_user['role']
            }
        }), 200
    return jsonify({'error': 'Failed to update user'}), 500

@profile_bp.route('/profile/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_profile(user_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
        return jsonify({'error': 'Invalid token identity'}), 401
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized: You can only delete your own profile'}), 403

    """Delete a user by ID."""
    if not user_manager.get_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404
    if user_manager.delete_user(user_id):
        log_admin_action(0, 'delete_user', 'user', user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete user'}), 500

@profile_bp.route('/search', methods=['GET'])
@jwt_required()
def search_profiles():
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
        return jsonify({'error': 'Invalid token identity'}), 401

    nom = request.args.get('nom', '').strip()
    filiere = request.args.get('filiere', '').strip()
    competence = request.args.get('competence', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    profiles, total = user_manager.search_users(
        nom=nom,
        filiere=filiere,
        competence=competence,
        exclude_user_id=current_user_id,
        page=page,
        per_page=per_page
    )
    results = []
    for p in profiles:
        competences_list = [c.strip() for c in p['competences'].split(',') if c.strip()] if p['competences'] else []
        results.append({
            'id': p['id'],
            'last_name': p['last_name'],
            'first_name': p['first_name'],
            'email': p['email'],
            'department': p['department'],
            'skills': competences_list,
            'photo': p['photo'],
            'role': p['role']
        })
    return jsonify({
        'results': results,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200