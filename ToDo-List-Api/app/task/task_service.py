from flask import current_app
from bson.objectid import ObjectId
from marshmallow import ValidationError
from app.schemas.schema import PaginationSchema, TaskSchema
from app.util.util import util

class TaskService:

    # Validation methods for handling pagination and task data
    @staticmethod
    def validate_list_tasks(request):
        """Validates pagination parameters from the request using PaginationSchema."""
        schema = PaginationSchema()
        try:
            data = schema.load(request.args)
            return data, None
        except ValidationError as err:
            return None, util.error_response("Validation failed", err.messages)

    @staticmethod
    def validate_create_task(request):
        """Validates task data (title and description) from the request using TaskSchema."""
        schema = TaskSchema()
        try:
            data = schema.load(request.get_json())
            return data, None
        except ValidationError as err:
            return None, util.error_response("Validation failed", err.messages)

    @staticmethod
    def get_test():
        """Test function to verify service functionality."""
        return "test"

    # Core CRUD operations for Task management
    @staticmethod
    def create_task(user_id, request):
        """Creates a new task for the specified user and stores it in the database."""
        validated_data, error_response = TaskService.validate_create_task(request)
        if error_response:
            return error_response

        title = validated_data['title']
        description = validated_data['description']

        db = current_app.config['Todo_List_Bd']
        task_collection = db.tasks

        # Task data structure to be stored in MongoDB
        task_data = {
            "user_id": ObjectId(user_id),
            "title": title,
            "description": description
        }
        result = task_collection.insert_one(task_data)

        # Prepare the response with the details of the created task
        created_task = {
            "id": str(result.inserted_id),
            "title": title,
            "description": description
        }
        
        return util.success_response("Task created successfully", created_task, 201)

    @staticmethod
    def list_tasks(user_id, request):
        """Retrieves a paginated list of tasks for the authenticated user."""
        pagination_data, error_response = TaskService.validate_list_tasks(request)
        if error_response:
            return error_response

        page = pagination_data['page']
        limit = pagination_data['limit']

        db = current_app.config['Todo_List_Bd']
        task_collection = db.tasks

        # Count total tasks for the user and calculate the skip value for pagination
        total_tasks = task_collection.count_documents({"user_id": ObjectId(user_id)})
        skip = (page - 1) * limit

        # Query tasks with pagination applied
        tasks = task_collection.find({"user_id": ObjectId(user_id)}).skip(skip).limit(limit)

        # Convert tasks to JSON format
        task_list = [
            {
                "id": str(task["_id"]),
                "title": task["title"],
                "description": task["description"]
            }
            for task in tasks
        ]

        response = {
            "data": task_list,
            "page": page,
            "limit": limit,
            "total": total_tasks
        }

        return util.success_response("Tasks retrieved successfully", response)

    @staticmethod
    def update_task(user_id, task_id, request):
        """Updates an existing task if it belongs to the authenticated user."""
        # Check if task_id is a valid ObjectId
        if not ObjectId.is_valid(task_id):
            return util.error_response("Bad Request", {"task_id": "Task ID is not valid"}, 400)

        # Validate the task data to be updated
        validated_data, validation_error = TaskService.validate_create_task(request)
        if validation_error:
            return validation_error

        title = validated_data.get('title')
        description = validated_data.get('description')

        db = current_app.config['Todo_List_Bd']
        task_collection = db.tasks

        # Retrieve task to verify ownership
        task = task_collection.find_one({"_id": ObjectId(task_id), "user_id": ObjectId(user_id)})
        if not task:
            return util.error_response("Forbidden", {"message": "You do not have permission to update this item"}, 403)

        # Create dictionary with updated data
        updated_data = {}
        if title:
            updated_data["title"] = title
        if description:
            updated_data["description"] = description

        # Update task in the database
        task_collection.update_one({"_id": ObjectId(task_id)}, {"$set": updated_data})

        # Prepare response with updated task details
        updated_task = {
            "id": task_id,
            "title": updated_data.get("title", task["title"]),
            "description": updated_data.get("description", task["description"])
        }

        return util.success_response("Task updated successfully", updated_task)

    @staticmethod
    def delete_task(user_id, task_id):
        """Deletes a task if it exists and belongs to the authenticated user."""
        # Validate that task_id is a valid ObjectId
        if not ObjectId.is_valid(task_id):
            return util.error_response("Bad Request", {"task_id": "Task ID is not valid"}, 400)

        db = current_app.config['Todo_List_Bd']
        task_collection = db.tasks

        # Verify that the task exists
        task = task_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            return util.error_response("Not Found", {"message": "Task does not exist"}, 404)

        # Check that the task belongs to the user
        if task["user_id"] != ObjectId(user_id):
            return util.error_response("Forbidden", {"message": "You do not have permission to delete this item"}, 403)

        # Delete the task
        task_collection.delete_one({"_id": ObjectId(task_id)})

        return util.success_response("Task deleted successfully", None, 200)  # Alternatively, 204 for no content response
