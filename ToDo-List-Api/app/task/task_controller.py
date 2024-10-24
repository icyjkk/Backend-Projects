from flask import Blueprint, request, jsonify,current_app
from app.decorators.decorators import token_required
from app.task.task_service import TaskService

task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/todos', methods=['POST'])
@token_required
def create_task(user_id):
    return TaskService.create_task(user_id,request)

@task_bp.route('/todos', methods=['GET'])
@token_required
def list_tasks(user_id):
    return TaskService.list_tasks(user_id,request)

@task_bp.route('/test', methods=['GET'])
def get_test():
    return TaskService.get_test()
