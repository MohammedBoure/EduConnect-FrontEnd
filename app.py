from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import datetime
from database import UserManager  # Assuming this is your database manager
from apis.auth import auth_bp
from apis.profile_ import profile_bp
from apis.messages import messages_bp
from apis.posts import posts_bp
from apis.comments import comments_bp
from apis.admin import admin_bp



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuration
app.config['JWT_SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'  # CHANGE THIS!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=10)

# Extensions
jwt = JWTManager(app)

# Initialize database
user_manager = UserManager()  # This triggers init_db()

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(profile_bp, url_prefix='/api')
app.register_blueprint(messages_bp, url_prefix='/api')
app.register_blueprint(posts_bp, url_prefix='/api')
app.register_blueprint(comments_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)