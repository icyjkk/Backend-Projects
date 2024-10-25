from flask import Blueprint, request, jsonify, current_app
from app.user.user_service import UserService

# Define the user blueprint with a URL prefix
user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/register', methods=['POST'])
def create_user():
    """Endpoint to register a new user.
    
    Expects a POST request with user details in JSON format.
    Returns a success message with JWT token if registration is successful.
    """
    return UserService.create_user(request)

@user_bp.route('/login', methods=['POST'])
def login():
    """Endpoint to log in a user.
    
    Expects a POST request with 'email' and 'password' fields in JSON format.
    Returns a success message with JWT token if login is successful.
    """
    return UserService.login(request.json.get('email'), request.json.get('password'))

@user_bp.route('/test', methods=['GET'])
def get_test():
    """Simple endpoint to verify service functionality."""
    return UserService.get_test()
