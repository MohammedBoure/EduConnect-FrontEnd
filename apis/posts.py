from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import datetime
from utils import safe_get_jwt_identity_as_int
from database import PostManager,AuditLogManager

post_manager = PostManager()
audit_log_manager = AuditLogManager()

def log_admin_action(admin_id, action, resource_type, resource_id, details=None):
    """Log administrative actions for auditing purposes."""
    audit_log_manager.log_action(admin_id, action, resource_type, resource_id, details)

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None: return jsonify({'error': 'Invalid token identity'}), 401

    """Create a new post on behalf of a user."""
    data = request.get_json()
    
    # Simulate user authentication by getting user_id from request
    current_user_id = data.get('user_id') if data else None
    if not current_user_id:
        return jsonify({'error': 'Missing user_id'}), 401

    title = data.get('title', '').strip() if data else ''
    content = data.get('content', '').strip() if data else ''
    image = data.get('image') if data else None

    if not title or not content:
        return jsonify({'error': 'Title and content cannot be empty'}), 400

    post_id = post_manager.create_post(current_user_id, content, title, image)
    if post_id:
        new_post = post_manager.get_post_by_id(post_id)
        if new_post:
            # Convert tuple to dict for consistent access
            post_data = {
                'id': new_post[0],
                'title': new_post[1],
                'content': new_post[2],
                'image': new_post[3],
                'created_at': new_post[4].isoformat() + "Z" if isinstance(new_post[4], datetime.datetime) else str(new_post[4]),
                'user_id': new_post[5],
                'author': {
                    'first_name': new_post[6],
                    'last_name': new_post[7],
                    'photo': new_post[8]
                }
            }
        else:
            post_data = {
                'id': post_id,
                'title': title,
                'content': content,
                'image': image,
                'created_at': datetime.datetime.utcnow().isoformat() + "Z",
                'user_id': current_user_id,
                'author': None
            }
        return jsonify({'message': 'Post created successfully', 'post': post_data}), 201

    return jsonify({'error': 'Failed to create post'}), 500

@posts_bp.route('/posts/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_posts_authenticated(user_id):
    _ = safe_get_jwt_identity_as_int()
    return get_user_posts_public(user_id)

@posts_bp.route('/posts/public/user/<int:user_id>', methods=['GET'])
def get_user_posts_public(user_id):
    if not post_manager.get_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    posts, total = post_manager.get_posts_by_user(user_id, page, per_page)

    post_list = []
    for p in posts:
        post_dict = {
            'id': p[0],  # p.id
            'title': p[1],
            'content': p[2],
            'image': p[3],
            'created_at': p[4].isoformat() + "Z" if isinstance(p[4], datetime.datetime) else str(p[4]),
            'user_id': p[5],
            'author': {
                'first_name': p[6],
                'last_name': p[7],
                'photo': p[8]
            }
        }
        post_list.append(post_dict)

    return jsonify({
        'posts': post_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200


@posts_bp.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None: return jsonify({'error': 'Invalid token identity'}), 401

    """Update an existing post."""
    post = post_manager.get_post_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    data = request.get_json()
    title = data.get('title', '').strip() if data else None
    content = data.get('content', '').strip() if data else None
    image = data.get('image') if data else None

    if title == '' or content == '':
        return jsonify({'error': 'Title and content cannot be empty'}), 400

    if post_manager.update_post(post_id, title, content, image):
        log_admin_action(0, 'update_post', 'post', post_id, f"Updated title: {title[:50] if title else ''}, content: {content[:50] if content else ''}")
        updated_post = post_manager.get_post_by_id(post_id)
        post_data = {
            'id': updated_post[0],
            'title': updated_post[1],
            'content': updated_post[2],
            'image': updated_post[3],
            'created_at': updated_post[4],
            'user_id': updated_post[5],
            'author': {
                'first_name': updated_post[6],
                'last_name': updated_post[7],
                'photo': updated_post[8]
            }
        }
        return jsonify({'message': 'Post updated successfully', 'post': post_data}), 200
    return jsonify({'error': 'Failed to update post'}), 500


@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None: return jsonify({'error': 'Invalid token identity'}), 401

    """Delete a post by ID."""
    if not post_manager.get_post_by_id(post_id):
        return jsonify({'error': 'Post not found'}), 404
    if post_manager.delete_post(post_id):
        log_admin_action(0, 'delete_post', 'post', post_id)
        return jsonify({'message': 'Post deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete post'}), 500