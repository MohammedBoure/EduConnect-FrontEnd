from flask import Blueprint, request, jsonify
from database import UserManager, PostManager, CommentManager, MessageManager, AuditLogManager
import datetime
from dateutil.parser import isoparse

admin_bp = Blueprint('admin', __name__)
user_manager = UserManager()
post_manager = PostManager()
comment_manager = CommentManager()
message_manager = MessageManager()
audit_log_manager = AuditLogManager()

def log_admin_action(admin_id, action, resource_type, resource_id, details=None):
    """Log administrative actions for auditing purposes."""
    audit_log_manager.log_action(admin_id, action, resource_type, resource_id, details)

# --- Admin User Management ---

@admin_bp.route('/admin/users', methods=['GET'])
def list_users():
    """Retrieve a paginated list of all users."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    users, total = user_manager.get_all_users(page, per_page)
    user_list = [{
        'id': user['id'],
        'last_name': user['last_name'],
        'first_name': user['first_name'],
        'email': user['email'],
        'department': user['department'],
        'skills': [skill.strip() for skill in user['skills'].split(',') if skill.strip()] if user['skills'] else [],
        'photo': user['photo'],
        'role': user['role']
    } for user in users]

    return jsonify({
        'users': user_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200

@admin_bp.route('/admin/users/<int:user_id>', methods=['GET'])
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

@admin_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
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

@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user by ID."""
    if not user_manager.get_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404
    if user_manager.delete_user(user_id):
        log_admin_action(0, 'delete_user', 'user', user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete user'}), 500

# --- Admin Post Management ---
@admin_bp.route('/admin/posts/create', methods=['POST'])
def create_post():
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

@admin_bp.route('/admin/posts', methods=['GET'])
def list_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    posts, total = post_manager.get_all_posts(page, per_page)
    post_list = [{
        'id': post[0],
        'title': post[1],
        'content': post[2],
        'image': post[3],
        'created_at': post[4].isoformat() + "Z" if isinstance(post[4], datetime.datetime) else str(post[4]),
        'user_id': post[5],
        'author': {
            'first_name': post[6],
            'last_name': post[7],
            'photo': post[8]
        }
    } for post in posts]

    return jsonify({
        'posts': post_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200
    
@admin_bp.route('/admin/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
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

@admin_bp.route('/admin/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by ID."""
    if not post_manager.get_post_by_id(post_id):
        return jsonify({'error': 'Post not found'}), 404
    if post_manager.delete_post(post_id):
        log_admin_action(0, 'delete_post', 'post', post_id)
        return jsonify({'message': 'Post deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete post'}), 500
# --- Admin Comment Management ---
@admin_bp.route('/admin/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    """Add a comment to a post."""
    try:
        new_comment = request.get_json()
        if 'content' not in new_comment or 'created_at' not in new_comment or 'user_id' not in new_comment:
            return jsonify({'error': 'Missing content, created_at, or user_id field'}), 400

        content = new_comment['content']
        created_at = new_comment['created_at']
        user_id = new_comment['user_id']

        # Validate and convert created_at to datetime
        if isinstance(created_at, str):
            try:
                created_at = isoparse(created_at)
            except ValueError:
                return jsonify({'error': 'Invalid date format for created_at'}), 400
        elif not isinstance(created_at, datetime.datetime):
            return jsonify({'error': 'created_at must be a datetime object or ISO format string'}), 400

        # Create the comment
        comment_id = comment_manager.create_comment(post_id=post_id, user_id=user_id, content=content, created_at=created_at)
        if comment_id:
            comment = comment_manager.get_comment_by_id(comment_id)
            if not comment:
                return jsonify({'error': 'Comment not found after creation'}), 500

            return jsonify({
                'message': 'Comment added successfully',
                'comment': {
                    'id': comment['id'],
                    'content': comment['content'],
                    'created_at': comment['created_at'].isoformat() + "Z",
                    'post_id': comment['post_id'],
                    'user_id': comment['user_id']
                }
            }), 201
        return jsonify({'error': 'Failed to create comment'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@admin_bp.route('/admin/comments', methods=['GET'])
def list_comments():
    """Retrieve a paginated list of all comments."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    comments, total = comment_manager.get_all_comments(page, per_page)
    comment_list = [{
        'id': comment['id'],
        'content': comment['content'],
        'created_at': comment['created_at'],
        'post_id': comment['post_id'],
        'user_id': comment['user_id'],
        'author': {
            'last_name': comment['last_name'],
            'first_name': comment['first_name'],
            'photo': comment['photo']
        }
    } for comment in comments]

    return jsonify({
        'comments': comment_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200

@admin_bp.route('/admin/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """Update an existing comment."""
    
    # Attempt to retrieve the comment by ID
    comment = comment_manager.get_comment_by_id(comment_id)
    
    # Return an error response if comment is not found
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    # Get the new content from the request JSON, ensure it's not empty
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    content = data.get('content', '').strip()
    if not content:
        return jsonify({'error': 'Comment content cannot be empty'}), 400

    # Attempt to update the comment in the database
    if comment_manager.update_comment(comment_id, content):
        # Log the admin action for auditing
        log_admin_action(0, 'update_comment', 'comment', comment_id, f"New content: {content[:50]}...")
        
        # Retrieve the updated comment to include in the response
        updated_comment = comment_manager.get_comment_by_id(comment_id)
        
        # Prepare the updated comment's data
        comment_data = {
            'id': updated_comment['id'],
            'content': updated_comment['content'],
            'created_at': updated_comment['created_at'],
            'post_id': updated_comment['post_id'],
            'user_id': updated_comment['user_id'],
            'author': {
                'last_name': updated_comment['last_name'],
                'first_name': updated_comment['first_name'],
                'photo': updated_comment['photo']
            }
        }
        
        # Return the success response with updated comment data
        return jsonify({'message': 'Comment updated successfully', 'comment': comment_data}), 200

    # If update fails, return an error response
    return jsonify({'error': 'Failed to update comment'}), 500

@admin_bp.route('/admin/comments/<int:comment_id>', methods=['DELETE','OPTIONS'])
def delete_comment(comment_id):
    """Delete a comment by ID."""
    if not comment_manager.get_comment_by_id(comment_id):
        return jsonify({'error': 'Comment not found'}), 404
    if comment_manager.delete_comment(comment_id):
        log_admin_action(0, 'delete_comment', 'comment', comment_id)
        return jsonify({'message': 'Comment deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete comment'}), 500

# --- Admin Message Management ---

@admin_bp.route('/admin/messages', methods=['GET'])
def list_messages():
    """Retrieve a paginated list of all messages."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)

    messages, total = message_manager.get_all_messages(page, per_page)
    message_list = [{
        'id': message['id'],
        'content': message['content'],
        'sender_id': message['sender_id'],
        'receiver_id': message['receiver_id'],
        'created_at': message['created_at']
    } for message in messages]

    return jsonify({
        'messages': message_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200

@admin_bp.route('/admin/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    """Delete a message by ID."""
    if not message_manager.get_message_by_id(message_id):
        return jsonify({'error': 'Message not found'}), 404
    if message_manager.delete_message(message_id):
        log_admin_action(0, 'delete_message', 'message', message_id)
        return jsonify({'message': 'Message deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete message'}), 500

@admin_bp.route('/admin/messages', methods=['POST'])
def send_message():
    """Send a new message from one user to another."""
    data = request.get_json()
    if not data or not data.get('sender_id') or not data.get('receiver_id') or not str(data.get('content', '')).strip():
        return jsonify({'error': 'Sender ID, receiver ID, and non-empty content are required'}), 400

    try:
        sender_id = int(data['sender_id'])
        receiver_id = int(data['receiver_id'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid sender_id or receiver_id format'}), 400

    if sender_id == receiver_id:
        return jsonify({'error': 'Cannot send messages to yourself'}), 400

    if not user_manager.get_user_by_id(receiver_id):
        return jsonify({'error': 'Receiver not found'}), 404

    content = str(data['content']).strip()
    message_id = message_manager.send_message(sender_id, receiver_id, content)

    if message_id:
        sent_message = message_manager.get_message_by_id(message_id)
        if sent_message:
            msg_data = {
                'id': sent_message['id'],
                'content': sent_message['content'],
                'sender_id': sent_message['sender_id'],
                'receiver_id': sent_message['receiver_id'],
                'created_at': sent_message['created_at'].isoformat() + "Z"
                              if isinstance(sent_message.get('created_at'), datetime.datetime)
                              else str(sent_message.get('created_at'))
            }
        else:
            msg_data = {
                'id': message_id,
                'content': content,
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'created_at': datetime.datetime.utcnow().isoformat() + "Z"
            }
        return jsonify({'message': 'Message sent successfully', 'sent_message': msg_data}), 201

    return jsonify({'error': 'Failed to send message'}), 500

@admin_bp.route('/admin/messages/<int:other_user_id>', methods=['POST'])
def get_messages(other_user_id):
    """Retrieve messages between two users with pagination."""
    data = request.get_json()
    current_user_id = data.get('user_id') if data else None
    if current_user_id is None:
        return jsonify({'error': 'Missing user_id'}), 401

    if not user_manager.get_user_by_id(other_user_id):
        return jsonify({'error': 'Other user not found'}), 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)

    messages, total = message_manager.get_messages_between_users(current_user_id, other_user_id, page, per_page)
    messages.reverse()

    message_list = [{
        'id': message['id'],
        'content': message['content'],
        'sender_id': message['sender_id'],
        'receiver_id': message['receiver_id'],
        'created_at': message['created_at'].isoformat() + "Z"
                      if isinstance(message.get('created_at'), datetime.datetime)
                      else str(message.get('created_at'))
    } for message in messages]

    return jsonify({
        'messages': message_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200