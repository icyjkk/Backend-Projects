from flask import Blueprint, request, jsonify,current_app
from app.user.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/register', methods=['POST'])
def create_user():

    data = request.json
    return UserService.create_user(data.get('name'),data.get('email'),data.get('password'))


@user_bp.route('/test', methods=['GET'])
def get_test():
    
    return UserService.get_test()
