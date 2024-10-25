from flask import Blueprint, request, jsonify, current_app
from app.decorators.decorators import token_required
from app.task.task_service import TaskService

# Blueprint for task-related routes
task_bp = Blueprint('task', __name__, url_prefix='/task')

# Route to create a new task (requires token authentication)
@task_bp.route('/todos', methods=['POST'])
@token_required
def create_task(user_id):
    return TaskService.create_task(user_id, request)

# Route to list all tasks for the authenticated user (requires token authentication)
@task_bp.route('/todos', methods=['GET'])
@token_required
def list_tasks(user_id):
    return TaskService.list_tasks(user_id, request)

# Route to update an existing task by ID (requires token authentication)
@task_bp.route('/todos/<task_id>', methods=['PUT'])
@token_required
def update_task(user_id, task_id):
    return TaskService.update_task(user_id, task_id, request)

# Route to delete a task by ID (requires token authentication)
@task_bp.route('/todos/<task_id>', methods=['DELETE'])
@token_required
def delete_task(user_id, task_id):
    return TaskService.delete_task(user_id, task_id)

# Test route to verify that the service is running
@task_bp.route('/test', methods=['GET'])
def get_test():
    return TaskService.get_test()
