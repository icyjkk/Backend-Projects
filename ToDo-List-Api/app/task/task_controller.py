from flask import Blueprint, request, jsonify, current_app
from app.decorators.decorators import token_required
from app.task.task_service import TaskService

# Blueprint for task-related routes, with a URL prefix for easier route organization
task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/todos', methods=['POST'])
@token_required
def create_task(user_id):
    """
    Endpoint to create a new task (requires token authentication).
    
    - Expects a POST request with task data (e.g., title and description) in JSON format.
    - Returns the created task details if successful.
    """
    return TaskService.create_task(user_id, request)

@task_bp.route('/todos', methods=['GET'])
@token_required
def list_tasks(user_id):
    """
    Endpoint to list all tasks for the authenticated user (requires token authentication).
    
    - Supports pagination.
    - Returns a paginated list of tasks for the authenticated user.
    """
    return TaskService.list_tasks(user_id, request)

@task_bp.route('/todos/<task_id>', methods=['PUT'])
@token_required
def update_task(user_id, task_id):
    """
    Endpoint to update an existing task by ID (requires token authentication).
    
    - Expects a PUT request with the updated task data in JSON format.
    - Returns the updated task details if successful.
    """
    return TaskService.update_task(user_id, task_id, request)

@task_bp.route('/todos/<task_id>', methods=['DELETE'])
@token_required
def delete_task(user_id, task_id):
    """
    Endpoint to delete a task by ID (requires token authentication).
    
    - Expects a DELETE request for a specific task ID.
    - Returns a success message if the task is deleted successfully.
    """
    return TaskService.delete_task(user_id, task_id)

@task_bp.route('/test', methods=['GET'])
def get_test():
    """Simple endpoint to verify service functionality."""
    return TaskService.get_test()
