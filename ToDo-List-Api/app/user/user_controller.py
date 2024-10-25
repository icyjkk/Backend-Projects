from flask import Blueprint, request, jsonify,current_app
from app.user.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/register', methods=['POST'])
def create_user():
    return UserService.create_user(request)

@user_bp.route('/login', methods=['POST'])
def login():
    return UserService.login(request.json.get('email'),request.json.get('password'))

@user_bp.route('/test', methods=['GET'])
def get_test():
    
    return UserService.get_test()
