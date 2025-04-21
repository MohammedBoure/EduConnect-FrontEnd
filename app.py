from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_cors import CORS
# Import ValueError for safe casting
from sqlalchemy.exc import IntegrityError # For more specific db errors if needed

app = Flask(__name__)
# Allow requests from any origin for /api/* routes (adjust for production)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- Configuration ---
app.config['JWT_SECRET_KEY'] = 'your-super-secret-and-long-key-change-me!' # CHANGE THIS!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_directory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Extensions ---
db = SQLAlchemy(app)
jwt = JWTManager(app)

# --- Models ---
class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False) # Store hash
    filiere = db.Column(db.String(50), nullable=False)
    competences = db.Column(db.String(255), nullable=False) # Stored as comma-separated string
    photo = db.Column(db.String(255), nullable=True) # Allow null for photo

    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic', cascade="all, delete-orphan")
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic', cascade="all, delete-orphan")

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id', ondelete='CASCADE'), nullable=False)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id', ondelete='CASCADE'), nullable=False)


# --- Database Initialization ---
# Use Flask-Migrate for managing database schema changes in a real app
with app.app_context():
    db.create_all() # Creates tables if they don't exist


# --- Helper Function for Safe Int Conversion ---
def safe_get_jwt_identity_as_int():
    """Gets JWT identity and safely converts to int, returns None on failure."""
    identity_str = get_jwt_identity()
    try:
        return int(identity_str)
    except (ValueError, TypeError):
        # Log this error in a real application
        print(f"Error: Could not convert JWT identity '{identity_str}' to int.")
        return None

# --- Routes ---

# User Registration
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['nom', 'prenom', 'email', 'mot_de_passe', 'filiere', 'competences']

    if not data or not all(field in data and data[field] for field in required_fields):
        # Added check for non-empty values
        return jsonify({'error': 'All fields are required and cannot be empty'}), 400

    if Utilisateur.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409 # 409 Conflict is more specific

    try:
        hashed_password = generate_password_hash(data['mot_de_passe'])
        # Ensure competences is stored as string
        competences_str = ','.join(data['competences']) if isinstance(data['competences'], list) else str(data['competences'])

        new_user = Utilisateur(
            nom=data['nom'],
            prenom=data['prenom'],
            email=data['email'],
            mot_de_passe=hashed_password,
            filiere=data['filiere'],
            competences=competences_str,
            photo=data.get('photo') # Safely get photo if provided
        )
        db.session.add(new_user)
        db.session.commit()
        # Return user info (excluding password) upon successful registration
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': new_user.id,
                'nom': new_user.nom,
                'prenom': new_user.prenom,
                'email': new_user.email
            }
            }), 201
    except IntegrityError as ie: # Catch potential db constraint errors
         db.session.rollback()
         print(f"Database Integrity Error: {ie}")
         return jsonify({'error': 'Database error during registration.'}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Registration Error: {e}") # Log the actual error
        return jsonify({'error': f"An unexpected error occurred: {e}"}), 500

# User Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('mot_de_passe'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = Utilisateur.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.mot_de_passe, data['mot_de_passe']):
        # Identity is stored as string, conversion happens where needed
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'user_id': user.id # Send user ID back for convenience
            }), 200
    else: # More specific feedback (without revealing too much)
        return jsonify({'error': 'Invalid email or password'}), 401

# Profile Management
@app.route('/api/profile/<int:user_id>', methods=['GET'])
@jwt_required() # Make getting profiles require login too? Optional.
def get_profile(user_id):
    # Consider if any logged-in user can view any profile, or only their own/connections
    user = Utilisateur.query.get_or_404(user_id, description="User not found")
    # Convert competences back to list for frontend if needed
    competences_list = user.competences.split(',') if user.competences else []
    return jsonify({
        'id': user.id,
        'nom': user.nom,
        'prenom': user.prenom,
        'email': user.email, # Consider if email should be public
        'filiere': user.filiere,
        'competences': competences_list, # Send as list
        'photo': user.photo
    }), 200

@app.route('/api/profile/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_profile(user_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
         return jsonify({'error': 'Invalid token identity'}), 401
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized: You can only update your own profile'}), 403

    user = Utilisateur.query.get(user_id) # No need for 404, auth check already ensures user exists if IDs match
    if not user: # Should not happen if auth is correct, but good check
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No update data provided'}), 400

    try:
        # Update fields selectively
        if 'nom' in data: user.nom = data['nom']
        if 'prenom' in data: user.prenom = data['prenom']
        # Add email update possibility? Requires care (verification)
        if 'filiere' in data: user.filiere = data['filiere']
        if 'competences' in data:
            # Ensure it's stored as string
            user.competences = ','.join(data['competences']) if isinstance(data['competences'], list) else str(data['competences'])
        if 'photo' in data: user.photo = data['photo']
        # Add password update? Requires current password verification

        db.session.commit()
        # Return updated profile
        competences_list = user.competences.split(',') if user.competences else []
        return jsonify({
             'message': 'Profile updated successfully',
             'user': {
                'id': user.id,
                'nom': user.nom,
                'prenom': user.prenom,
                'filiere': user.filiere,
                'competences': competences_list,
                'photo': user.photo
             }
             }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Profile Update Error: {e}")
        return jsonify({'error': f'An error occurred during profile update: {e}'}), 500

@app.route('/api/profile/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_profile(user_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
         return jsonify({'error': 'Invalid token identity'}), 401
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized: You can only delete your own profile'}), 403

    user = Utilisateur.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        # Cascading delete should handle related posts/messages if configured
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Profile deleted successfully'}), 200 # Or 204 No Content
    except Exception as e:
        db.session.rollback()
        print(f"Profile Delete Error: {e}")
        return jsonify({'error': f'An error occurred during profile deletion: {e}'}), 500

# Profile Search
@app.route('/api/search', methods=['GET'])
@jwt_required() # Should search require login?
def search_profiles():
    # Consider adding pagination (page, per_page args) for large results
    nom = request.args.get('nom', '').strip()
    filiere = request.args.get('filiere', '').strip()
    competence = request.args.get('competence', '').strip() # Search by competence

    query = Utilisateur.query

    # Exclude the current user from search results?
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id:
        query = query.filter(Utilisateur.id != current_user_id)


    if nom:
        # Search in both nom and prenom
        query = query.filter(Utilisateur.nom.ilike(f"%{nom}%") | Utilisateur.prenom.ilike(f"%{nom}%"))
    if filiere:
        query = query.filter(Utilisateur.filiere.ilike(f"%{filiere}%"))
    if competence:
         # Search if competence is within the comma-separated string
         query = query.filter(Utilisateur.competences.ilike(f"%{competence}%"))

    # Add pagination example
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_profiles = query.paginate(page=page, per_page=per_page, error_out=False)
    profiles = paginated_profiles.items

    results = []
    for p in profiles:
        competences_list = p.competences.split(',') if p.competences else []
        results.append({
            'id': p.id, # Important to return ID for chat selection
            'nom': p.nom,
            'prenom': p.prenom,
            'filiere': p.filiere,
            'competences': competences_list, # Send as list
            'photo': p.photo
        })

    return jsonify({
        'results': results,
        'total': paginated_profiles.total,
        'page': paginated_profiles.page,
        'pages': paginated_profiles.pages,
        'per_page': paginated_profiles.per_page
        }), 200


# --- Chat Functionality ---

@app.route('/api/messages', methods=['POST'])
@jwt_required()
def send_message():
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
         return jsonify({'error': 'Invalid token identity'}), 401

    data = request.get_json()

    if not data or not data.get('receiver_id') or not data.get('content'):
        return jsonify({'error': 'receiver_id and content are required'}), 400

    # Validate receiver_id type and value
    try:
        receiver_id = int(data['receiver_id'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid receiver_id format'}), 400

    if receiver_id == current_user_id:
         return jsonify({'error': 'Cannot send messages to yourself'}), 400

    receiver = Utilisateur.query.get(receiver_id)
    if not receiver:
        return jsonify({'error': 'Receiver not found'}), 404

    try:
        message = Message(
            content=data['content'].strip(), # Trim whitespace
            sender_id=current_user_id,       # Use the converted int ID
            receiver_id=receiver_id
        )
        db.session.add(message)
        db.session.commit()
        # Optionally return the created message
        return jsonify({
             'message': 'Message sent successfully',
             'sent_message': {
                 'id': message.id,
                 'content': message.content,
                 'sender_id': message.sender_id,
                 'receiver_id': message.receiver_id,
                 'created_at': message.created_at.isoformat()
             }
             }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Send Message Error: {e}")
        return jsonify({'error': f'An error occurred while sending the message: {e}'}), 500

@app.route('/api/messages/<int:other_user_id>', methods=['GET'])
@jwt_required()
def get_messages(other_user_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
         return jsonify({'error': 'Invalid token identity'}), 401

    # Ensure other user exists (optional but good practice)
    other_user = Utilisateur.query.get(other_user_id)
    if not other_user:
        return jsonify({'error': 'Other user not found'}), 404

    # Add pagination for messages too
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int) # Fetch more messages per page typically

    try:
        # Query using the converted int ID
        message_query = Message.query.filter(
            ((Message.sender_id == current_user_id) & (Message.receiver_id == other_user_id)) |
            ((Message.sender_id == other_user_id) & (Message.receiver_id == current_user_id))
        ).order_by(Message.created_at.desc()) # Order by desc for pagination (newest first)

        paginated_messages = message_query.paginate(page=page, per_page=per_page, error_out=False)
        messages = paginated_messages.items

        # Reverse the list for chronological display in frontend
        messages.reverse()

        message_list = [{
            'id': m.id,
            'content': m.content,
            'sender_id': m.sender_id,
            'receiver_id': m.receiver_id,
            'created_at': m.created_at.isoformat()
        } for m in messages]

        return jsonify({
            'messages': message_list,
            'total': paginated_messages.total,
            'page': paginated_messages.page,
            'pages': paginated_messages.pages,
            'per_page': paginated_messages.per_page
            }), 200
    except Exception as e:
        print(f"Get Messages Error: {e}")
        return jsonify({'error': f'An error occurred while retrieving messages: {e}'}), 500


# --- Post Functionality ---

@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
         return jsonify({'error': 'Invalid token identity'}), 401

    data = request.get_json()
    if not data or not data.get('content') or not data['content'].strip():
        return jsonify({'error': 'Content is required and cannot be empty'}), 400

    try:
        post = Post(
            content=data['content'].strip(),
            user_id=current_user_id # Use the converted int ID
        )
        db.session.add(post)
        db.session.commit()
        return jsonify({
             'message': 'Post created successfully',
             'post': {
                'id': post.id,
                'content': post.content,
                'created_at': post.created_at.isoformat(),
                'user_id': post.user_id
             }
             }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Create Post Error: {e}")
        return jsonify({'error': f'An error occurred while creating the post: {e}'}), 500

@app.route('/api/posts/user/<int:user_id>', methods=['GET']) # Changed path slightly for clarity
@jwt_required() # Require login to view posts? Optional.
def get_user_posts(user_id):
    # Add pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Ensure user exists
    user = Utilisateur.query.get_or_404(user_id, description="User not found")

    try:
        post_query = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc())
        paginated_posts = post_query.paginate(page=page, per_page=per_page, error_out=False)
        posts = paginated_posts.items

        post_list = [{
            'id': p.id,
            'content': p.content,
            'created_at': p.created_at.isoformat(),
            'user_id': p.user_id,
            # Optionally include author info
            'author': {
                'nom': p.author.nom,
                'prenom': p.author.prenom
            }
        } for p in posts]

        return jsonify({
            'posts': post_list,
            'total': paginated_posts.total,
            'page': paginated_posts.page,
            'pages': paginated_posts.pages,
            'per_page': paginated_posts.per_page
            }), 200
    except Exception as e:
        print(f"Get User Posts Error: {e}")
        return jsonify({'error': f'An error occurred while retrieving posts: {e}'}), 500

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
         return jsonify({'error': 'Invalid token identity'}), 401

    post = Post.query.get_or_404(post_id, description="Post not found")

    # Authorization check using converted int ID
    if post.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized: You can only update your own posts'}), 403

    data = request.get_json()
    if not data or not data.get('content') or not data['content'].strip():
        return jsonify({'error': 'Content is required and cannot be empty'}), 400

    try:
        post.content = data['content'].strip()
        db.session.commit()
        return jsonify({
            'message': 'Post updated successfully',
            'post': {
                'id': post.id,
                'content': post.content,
                'created_at': post.created_at.isoformat(),
                'user_id': post.user_id
            }
            }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Update Post Error: {e}")
        return jsonify({'error': f'An error occurred while updating the post: {e}'}), 500

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = safe_get_jwt_identity_as_int()
    if current_user_id is None:
         return jsonify({'error': 'Invalid token identity'}), 401

    post = Post.query.get_or_404(post_id, description="Post not found")

    # Authorization check using converted int ID
    if post.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized: You can only delete your own posts'}), 403

    try:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'}), 200 # Or 204 No Content
    except Exception as e:
        db.session.rollback()
        print(f"Delete Post Error: {e}")
        return jsonify({'error': f'An error occurred while deleting the post: {e}'}), 500



@app.route('/')
def index():
    return render_template('message_and_search.html')


# --- Main Execution ---
if __name__ == '__main__':
    # Consider using environment variables for host/port/debug
    app.run(debug=True, host='0.0.0.0', port=5000) # Example: Run on all interfaces, port 5000