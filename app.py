from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request, get_jwt # Added verify_jwt_in_request, get_jwt for optional auth
import datetime # Keep this one
# Remove the second import of datetime if it exists
# from datetime import datetime # Remove this duplicate if present
from flask_cors import CORS
import database  # Import database functions

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuration
app.config['JWT_SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'  # CHANGE THIS!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1) # Example: Token expires in 1 day

# Extensions
jwt = JWTManager(app)

# Initialize database
database.init_db()

# --- Helper Functions ---
def safe_get_jwt_identity_as_int():
    """Gets JWT identity and safely converts to int, returns None on failure."""
    try:
        identity_str = get_jwt_identity()
        return int(identity_str)
    except Exception as e: # Catch broader exceptions during JWT processing
        print(f"Error getting or converting JWT identity: {e}")
        return None


def get_optional_jwt_identity_as_int():
    """Tries to get JWT identity if present, returns int or None."""
    try:
        # verify_jwt_in_request checks for a valid token but doesn't enforce it
        # The optional=True flag prevents it from raising NoAuthorizationError if no token is present
        verify_jwt_in_request(optional=True)
        # If a token was present and valid, get the identity
        return safe_get_jwt_identity_as_int()
    except Exception as e:
        # Handle potential errors during optional verification or identity retrieval
        print(f"Optional JWT check failed or no token present: {e}")
        return None


# --- User and Profile Routes ---

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['nom', 'prenom', 'email', 'mot_de_passe', 'filiere', 'competences']

    if not data or not all(field in data and data[field] for field in required_fields):
        return jsonify({'error': 'All fields are required and cannot be empty'}), 400

    if database.get_user_by_email(data['email']):
        return jsonify({'error': 'Email already exists'}), 409

    # Ensure competences is stored as a string if it's passed as a list
    competences_data = data['competences']
    if isinstance(competences_data, list):
        competences_str = ','.join(filter(None, competences_data)) # Filter out empty strings
    else:
        competences_str = str(competences_data or '') # Handle None or empty string

    user_id = database.create_user(
        nom=data['nom'],
        prenom=data['prenom'],
        email=data['email'],
        mot_de_passe=data['mot_de_passe'], # Assume hashing is done in create_user
        filiere=data['filiere'],
        competences=competences_str,
        photo=data.get('photo')
    )
    if user_id:
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user_id,
                'nom': data['nom'],
                'prenom': data['prenom'],
                'email': data['email']
            }
        }), 201
    return jsonify({'error': 'Database error during registration'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('mot_de_passe'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = database.get_user_by_email(data['email'])
    # Assume check_password_hash is in database.py or import it
    # Make sure user exists AND password check passes
    if user and database.check_password_hash(user['mot_de_passe'], data['mot_de_passe']):
        access_token = create_access_token(identity=str(user['id']))
        return jsonify({
            'access_token': access_token,
            'user_id': user['id'] # Return user_id for convenience
        }), 200
    return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = database.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    # Safely split competences
    competences_list = [c.strip() for c in user['competences'].split(',') if c.strip()] if user['competences'] else []
    return jsonify({
        'id': user['id'],
        'nom': user['nom'],
        'prenom': user['prenom'],
        'email': user['email'], # Consider if email should be public
        'filiere': user['filiere'],
        'competences': competences_list,
        'photo': user['photo']
    }), 200


@app.route('/api/profile/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_profile(user_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
        return jsonify({'error': 'Invalid token identity'}), 401
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized: You can only update your own profile'}), 403

    user = database.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No update data provided'}), 400

    # Handle competences update (list to string)
    competences_data = data.get('competences')
    competences_str = None
    if competences_data is not None: # Check if 'competences' key exists in data
        if isinstance(competences_data, list):
             competences_str = ','.join(filter(None, competences_data))
        else:
             competences_str = str(competences_data or '') # Handle potential None or empty string

    update_payload = {}
    if data.get('nom') is not None: update_payload['nom'] = data['nom']
    if data.get('prenom') is not None: update_payload['prenom'] = data['prenom']
    if data.get('filiere') is not None: update_payload['filiere'] = data['filiere']
    if competences_str is not None: update_payload['competences'] = competences_str
    if data.get('photo') is not None: update_payload['photo'] = data['photo']
    # Add password update logic here if needed, ensuring proper hashing

    if not update_payload:
         return jsonify({'error': 'No valid update fields provided'}), 400

    success = database.update_user(user_id, **update_payload)

    if success:
        updated_user = database.get_user_by_id(user_id) # Fetch again to get current state
        competences_list = [c.strip() for c in updated_user['competences'].split(',') if c.strip()] if updated_user['competences'] else []
        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': updated_user['id'],
                'nom': updated_user['nom'],
                'prenom': updated_user['prenom'],
                'filiere': updated_user['filiere'],
                'competences': competences_list,
                'photo': updated_user['photo']
            }
        }), 200
    return jsonify({'error': 'An error occurred during profile update'}), 500

@app.route('/api/profile/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_profile(user_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
        return jsonify({'error': 'Invalid token identity'}), 401
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized: You can only delete your own profile'}), 403

    # Add cascading delete logic or checks in database.delete_user if needed
    if database.delete_user(user_id):
        return jsonify({'message': 'Profile deleted successfully'}), 200
    return jsonify({'error': 'An error occurred during profile deletion or user not found'}), 500

@app.route('/api/search', methods=['GET'])
@jwt_required() # Keep search protected for logged-in users
def search_profiles():
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
        return jsonify({'error': 'Invalid token identity'}), 401

    nom = request.args.get('nom', '').strip()
    filiere = request.args.get('filiere', '').strip()
    competence = request.args.get('competence', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    profiles, total = database.search_users(
        nom=nom,
        filiere=filiere,
        competence=competence,
        exclude_user_id=current_user_id, # Exclude self from search
        page=page,
        per_page=per_page
    )
    results = []
    for p in profiles:
        competences_list = [c.strip() for c in p['competences'].split(',') if c.strip()] if p['competences'] else []
        results.append({
            'id': p['id'],
            'nom': p['nom'],
            'prenom': p['prenom'],
            'filiere': p['filiere'],
            'competences': competences_list,
            'photo': p['photo']
        })
    return jsonify({
        'results': results,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200


# --- Messaging Routes ---

@app.route('/api/messages', methods=['POST'])
@jwt_required()
def send_message():
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None: return jsonify({'error': 'Invalid token identity'}), 401

    data = request.get_json()
    if not data or not data.get('receiver_id') or not data.get('content') or not str(data['content']).strip():
        return jsonify({'error': 'receiver_id and non-empty content are required'}), 400

    try:
        receiver_id = int(data['receiver_id'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid receiver_id format'}), 400

    if receiver_id == current_user_id:
        return jsonify({'error': 'Cannot send messages to yourself'}), 400

    if not database.get_user_by_id(receiver_id): # Check if receiver exists
        return jsonify({'error': 'Receiver user not found'}), 404

    content = str(data['content']).strip()
    message_id = database.send_message(current_user_id, receiver_id, content)

    if message_id:
        # Fetch the created message to get the timestamp from DB if possible
        # Otherwise, use current time (less accurate)
        sent_message = database.get_message_by_id(message_id) # Assumes this function exists
        if sent_message:
             msg_data = {
                'id': sent_message['id'],
                'content': sent_message['content'],
                'sender_id': sent_message['sender_id'],
                'receiver_id': sent_message['receiver_id'],
                'created_at': sent_message['created_at'].isoformat() if isinstance(sent_message.get('created_at'), datetime.datetime) else str(sent_message.get('created_at'))
            }
        else: # Fallback if get_message_by_id isn't available or fails
            msg_data = {
                'id': message_id,
                'content': content,
                'sender_id': current_user_id,
                'receiver_id': receiver_id,
                'created_at': datetime.datetime.utcnow().isoformat() + "Z" # Add Z for UTC
            }
        return jsonify({'message': 'Message sent successfully', 'sent_message': msg_data}), 201
    return jsonify({'error': 'An error occurred while sending the message'}), 500


@app.route('/api/messages/<int:other_user_id>', methods=['GET'])
@jwt_required()
def get_messages(other_user_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None: return jsonify({'error': 'Invalid token identity'}), 401

    if not database.get_user_by_id(other_user_id): # Check if other user exists
        return jsonify({'error': 'Other user not found'}), 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)

    messages, total = database.get_messages_between_users(current_user_id, other_user_id, page, per_page)

    # Ensure messages are returned in chronological order (oldest first)
    # If database returns newest first, reverse it here. If it returns oldest first, keep it.
    # Assuming database.get_messages_between_users returns newest first based on common practice for pagination:
    messages.reverse()

    message_list = [{
        'id': m['id'],
        'content': m['content'],
        'sender_id': m['sender_id'],
        'receiver_id': m['receiver_id'],
        # Ensure created_at is consistently formatted (ISO 8601 preferred)
        'created_at': m['created_at'].isoformat() + "Z" if isinstance(m.get('created_at'), datetime.datetime) else str(m.get('created_at'))
    } for m in messages]

    return jsonify({
        'messages': message_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200


# --- Post Routes ---

@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None: return jsonify({'error': 'Invalid token identity'}), 401

    data = request.get_json()
    content = data.get('content', '').strip() if data else ''
    if not content:
        return jsonify({'error': 'Post content cannot be empty'}), 400

    post_id = database.create_post(current_user_id, content)
    if post_id:
        # Fetch the created post to get accurate data including timestamp
        new_post = database.get_post_by_id(post_id) # Assumes this returns needed fields
        if new_post:
             post_data = {
                 'id': new_post['id'],
                 'content': new_post['content'],
                 'created_at': new_post['created_at'].isoformat() + "Z" if isinstance(new_post.get('created_at'), datetime.datetime) else str(new_post.get('created_at')),
                 'user_id': new_post['user_id'],
                 # Include author details if get_post_by_id provides them
                 'author': {
                    'nom': new_post.get('nom'), # Assuming get_post_by_id joins user table
                    'prenom': new_post.get('prenom')
                 } if new_post.get('nom') else None
             }
        else: # Fallback
             post_data = {
                 'id': post_id,
                 'content': content,
                 'created_at': datetime.datetime.utcnow().isoformat() + "Z",
                 'user_id': current_user_id
             }
        return jsonify({'message': 'Post created successfully', 'post': post_data}), 201
    return jsonify({'error': 'An error occurred while creating the post'}), 500

# MODIFIED: Endpoint for logged-in users (might have extra features later)
@app.route('/api/posts/user/<int:user_id>', methods=['GET'])
@jwt_required() # Requires login to view posts via this endpoint
def get_user_posts_authenticated(user_id):
    # Optional: Add checks specific to logged-in users if needed
    _ = safe_get_jwt_identity_as_int() # Verify token is valid even if not used directly here
    # Re-use the public logic
    return get_user_posts_public(user_id)

# NEW: Public endpoint for viewing user posts (no login required)
@app.route('/api/posts/public/user/<int:user_id>', methods=['GET'])
def get_user_posts_public(user_id):
    if not database.get_user_by_id(user_id): # Check if user exists
        return jsonify({'error': 'User not found'}), 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Assume database.get_posts_by_user fetches posts with author details (nom, prenom)
    posts, total = database.get_posts_by_user(user_id, page, per_page)

    post_list = [{
        'id': p['id'],
        'content': p['content'],
        'created_at': p['created_at'].isoformat() + "Z" if isinstance(p.get('created_at'), datetime.datetime) else str(p.get('created_at')),
        'user_id': p['user_id'],
        'author': { # Assuming the db function returns these joined fields
            'nom': p.get('nom'),
            'prenom': p.get('prenom'),
            'photo': p.get('photo') # Also include photo if available
        }
    } for p in posts]

    return jsonify({
        'posts': post_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None: return jsonify({'error': 'Invalid token identity'}), 401

    post = database.get_post_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    if post['user_id'] != current_user_id:
        return jsonify({'error': 'Unauthorized: You can only update your own posts'}), 403

    data = request.get_json()
    content = data.get('content', '').strip() if data else ''
    if not content:
        return jsonify({'error': 'Post content cannot be empty'}), 400

    if database.update_post(post_id, content):
        updated_post = database.get_post_by_id(post_id) # Fetch updated post
        if updated_post:
             post_data = {
                'id': updated_post['id'],
                'content': updated_post['content'],
                'created_at': updated_post['created_at'].isoformat() + "Z" if isinstance(updated_post.get('created_at'), datetime.datetime) else str(updated_post.get('created_at')),
                'user_id': updated_post['user_id'],
                 'author': {
                    'nom': updated_post.get('nom'),
                    'prenom': updated_post.get('prenom')
                 } if updated_post.get('nom') else None
            }
        else: # Fallback if fetch fails
            post_data = {'id': post_id, 'content': content} # Minimal info

        return jsonify({'message': 'Post updated successfully', 'post': post_data}), 200
    return jsonify({'error': 'An error occurred while updating the post'}), 500

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None: return jsonify({'error': 'Invalid token identity'}), 401

    post = database.get_post_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    if post['user_id'] != current_user_id:
        # Future enhancement: Allow admins or moderators to delete?
        return jsonify({'error': 'Unauthorized: You can only delete your own posts'}), 403

    # Consider deleting associated comments or handling foreign key constraints
    if database.delete_post(post_id):
        # Optionally: Delete related comments here if cascade delete isn't set up
        # database.delete_comments_by_post_id(post_id) # Assumes this function exists
        return jsonify({'message': 'Post deleted successfully'}), 200
    return jsonify({'error': 'An error occurred while deleting the post'}), 500


# --- Comment Routes ---

@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    """Adds a comment to a specific post."""
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
        return jsonify({'error': 'Invalid token identity'}), 401

    # Check if the post exists
    post = database.get_post_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    data = request.get_json()
    content = data.get('content', '').strip() if data else ''
    if not content:
        return jsonify({'error': 'Comment content cannot be empty'}), 400

    # Assume database.create_comment(post_id, user_id, content) returns the new comment's ID
    comment_id = database.create_comment(post_id, current_user_id, content)

    if comment_id:
        # Fetch the created comment to return full details including timestamp and author info
        new_comment = database.get_comment_by_id(comment_id) # Assume this joins user table for author
        if new_comment:
             comment_data = {
                'id': new_comment['id'],
                'content': new_comment['content'],
                'created_at': new_comment['created_at'].isoformat() + "Z" if isinstance(new_comment.get('created_at'), datetime.datetime) else str(new_comment.get('created_at')),
                'post_id': new_comment['post_id'],
                'user_id': new_comment['user_id'],
                'author': { # Assuming get_comment_by_id joins user table
                    'nom': new_comment.get('nom'),
                    'prenom': new_comment.get('prenom'),
                    'photo': new_comment.get('photo')
                }
            }
        else: # Fallback
             comment_data = {
                'id': comment_id,
                'content': content,
                'created_at': datetime.datetime.utcnow().isoformat() + "Z",
                'post_id': post_id,
                'user_id': current_user_id,
             }
        return jsonify({'message': 'Comment added successfully', 'comment': comment_data}), 201
    else:
        return jsonify({'error': 'Failed to add comment'}), 500

@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    """Gets comments for a specific post (publicly accessible)."""
    # Check if the post exists (optional but good practice)
    if not database.get_post_by_id(post_id):
         return jsonify({'error': 'Post not found'}), 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int) # Default comments per page

    # Assume database.get_comments_by_post returns (list_of_comments, total_count)
    # and each comment dict includes author info ('nom', 'prenom', 'photo')
    comments, total = database.get_comments_by_post(post_id, page, per_page)

    comment_list = [{
        'id': c['id'],
        'content': c['content'],
        'created_at': c['created_at'].isoformat() + "Z" if isinstance(c.get('created_at'), datetime.datetime) else str(c.get('created_at')),
        'post_id': c['post_id'],
        'user_id': c['user_id'],
        'author': {
            'nom': c.get('nom'),      # Safely get author details
            'prenom': c.get('prenom'),
            'photo': c.get('photo')
        }
    } for c in comments]

    return jsonify({
        'comments': comment_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200

@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    """Updates a specific comment."""
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
        return jsonify({'error': 'Invalid token identity'}), 401

    # Fetch the comment to check existence and ownership
    comment = database.get_comment_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    if comment['user_id'] != current_user_id:
        return jsonify({'error': 'Unauthorized: You can only update your own comments'}), 403

    data = request.get_json()
    content = data.get('content', '').strip() if data else ''
    if not content:
        return jsonify({'error': 'Comment content cannot be empty'}), 400

    # Assume database.update_comment(comment_id, content) returns True/False
    if database.update_comment(comment_id, content):
        # Fetch the updated comment to return
        updated_comment = database.get_comment_by_id(comment_id)
        if updated_comment:
            comment_data = {
                'id': updated_comment['id'],
                'content': updated_comment['content'],
                'created_at': updated_comment['created_at'].isoformat() + "Z" if isinstance(updated_comment.get('created_at'), datetime.datetime) else str(updated_comment.get('created_at')),
                'post_id': updated_comment['post_id'],
                'user_id': updated_comment['user_id'],
                'author': {
                    'nom': updated_comment.get('nom'),
                    'prenom': updated_comment.get('prenom'),
                    'photo': updated_comment.get('photo')
                }
            }
            return jsonify({'message': 'Comment updated successfully', 'comment': comment_data}), 200
        else: # Fallback if fetch fails
             return jsonify({'message': 'Comment updated successfully (fetch failed)', 'comment': {'id': comment_id, 'content': content}}), 200
    else:
        return jsonify({'error': 'Failed to update comment'}), 500

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """Deletes a specific comment."""
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
        return jsonify({'error': 'Invalid token identity'}), 401

    # Fetch the comment to check existence and ownership
    comment = database.get_comment_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    # Check ownership - Only the comment author can delete
    # Future: Post author might also be allowed to delete comments on their post
    # post = database.get_post_by_id(comment['post_id'])
    # if comment['user_id'] != current_user_id and (not post or post['user_id'] != current_user_id):
    if comment['user_id'] != current_user_id:
         return jsonify({'error': 'Unauthorized: You can only delete your own comments'}), 403

    # Assume database.delete_comment(comment_id) returns True/False
    if database.delete_comment(comment_id):
        return jsonify({'message': 'Comment deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete comment'}), 500


# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)