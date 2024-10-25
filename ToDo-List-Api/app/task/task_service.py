from flask import current_app
from bson.objectid import ObjectId
from marshmallow import ValidationError
from app.schemas.schema import PaginationSchema, TaskSchema
from app.util.util import util

class TaskService:

    # Validation methods for handling pagination and task data
    @staticmethod
    def validate_list_tasks(request):
        schema = PaginationSchema()
        try:
            data = schema.load(request.args)
            return data, None
        except ValidationError as err:
            return None, util.error_response("Validation failed", err.messages)

    @staticmethod
    def validate_create_task(request):
        schema = TaskSchema()
        try:
            data = schema.load(request.get_json())
            return data, None
        except ValidationError as err:
            return None, util.error_response("Validation failed", err.messages)

    @staticmethod
    def get_test():
        return "test"

    # Core CRUD operations for Task management
    @staticmethod
    def create_task(user_id, request):
        validated_data, error_response = TaskService.validate_create_task(request)
        if error_response:
            return error_response

        title = validated_data['title']
        description = validated_data['description']

        db = current_app.config['Todo_List_Bd']
        task_collection = db.tasks

        task_data = {
            "user_id": ObjectId(user_id),
            "title": title,
            "description": description
        }
        result = task_collection.insert_one(task_data)

        created_task = {
            "id": str(result.inserted_id),
            "title": title,
            "description": description
        }
        
        return util.success_response("Task created successfully", created_task, 201)

    @staticmethod
    def list_tasks(user_id, request):
        pagination_data, error_response = TaskService.validate_list_tasks(request)
        if error_response:
            return error_response

        page = pagination_data['page']
        limit = pagination_data['limit']

        db = current_app.config['Todo_List_Bd']
        task_collection = db.tasks

        total_tasks = task_collection.count_documents({"user_id": ObjectId(user_id)})
        skip = (page - 1) * limit

        tasks = task_collection.find({"user_id": ObjectId(user_id)}).skip(skip).limit(limit)

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
        if not ObjectId.is_valid(task_id):
            return util.error_response("Bad Request", {"task_id": "Task ID is not valid"}, 400)

        validated_data, validation_error = TaskService.validate_create_task(request)
        if validation_error:
            return validation_error

        title = validated_data.get('title')
        description = validated_data.get('description')

        db = current_app.config['Todo_List_Bd']
        task_collection = db.tasks

        task = task_collection.find_one({"_id": ObjectId(task_id), "user_id": ObjectId(user_id)})
        if not task:
            return util.error_response("Forbidden", {"message": "You do not have permission to update this item"}, 403)

        updated_data = {}
        if title:
            updated_data["title"] = title
        if description:
            updated_data["description"] = description

        task_collection.update_one({"_id": ObjectId(task_id)}, {"$set": updated_data})

        updated_task = {
            "id": task_id,
            "title": updated_data.get("title", task["title"]),
            "description": updated_data.get("description", task["description"])
        }

        return util.success_response("Task updated successfully", updated_task)

    @staticmethod
    def delete_task(user_id, task_id):
        if not ObjectId.is_valid(task_id):
            return util.error_response("Bad Request", {"task_id": "Task ID is not valid"}, 400)

        db = current_app.config['Todo_List_Bd']
        task_collection = db.tasks

        task = task_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            return util.error_response("Not Found", {"message": "Task does not exist"}, 404)

        if task["user_id"] != ObjectId(user_id):
            return util.error_response("Forbidden", {"message": "You do not have permission to delete this item"}, 403)

        task_collection.delete_one({"_id": ObjectId(task_id)})

        return util.success_response("Task deleted successfully", None, 200)  # You can also use 204 for no content response
