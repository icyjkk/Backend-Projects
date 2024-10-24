from flask import current_app
from bson.objectid import ObjectId
from marshmallow import ValidationError
from app.schemas.schema import PaginationSchema, TaskSchema
from app.util.util import util

class TaskService:

    @staticmethod
    def validate_list_tasks(request):
        schema = PaginationSchema()
        try:
            data = schema.load(request.args)  # Query params
            return data, None
        except ValidationError as err:
            return None, util.error_response("Validation failed", err.messages)

    @staticmethod
    def validate_create_task(request):
        schema = TaskSchema()
        try:
            data = schema.load(request.get_json())  # JSON body
            return data, None
        except ValidationError as err:
            return None, util.error_response("Validation failed", err.messages)

    @staticmethod
    def get_test():
        return "test"

    @staticmethod
    def create_task(user_id, request):
        
        # Validar los datos de la tarea
        validated_data, error_response = TaskService.validate_create_task(request)
        if error_response:
            return error_response  # Retorna el error si la validación falla

        # Extraer los valores validados
        title = validated_data['title']
        description = validated_data['description']

        # Acceder a la base de datos
        db = current_app.config['Todo_List_Bd']
        task_collection = db.tasks

        # Crear la tarea
        task_data = {
            "user_id": ObjectId(user_id),
            "title": title,
            "description": description
        }
        result = task_collection.insert_one(task_data)

        # Preparar la respuesta con los detalles de la tarea creada
        created_task = {
            "id": str(result.inserted_id),
            "title": title,
            "description": description
        }
        
        return util.success_response("Task created successfully", created_task,201)

    @staticmethod
    def list_tasks(user_id, request):
        
        # Validar los parámetros de paginación
        pagination_data, error_response = TaskService.validate_list_tasks(request)
        if error_response:
            return error_response  # Retorna el error si la validación falla

        # Extraer los valores de paginación
        page = pagination_data['page']
        limit = pagination_data['limit']

        # Acceder a la base de datos
        db = current_app.config['Todo_List_Bd']
        task_collection = db.tasks

        # Calcular el número total de tareas del usuario
        total_tasks = task_collection.count_documents({"user_id": ObjectId(user_id)})

        # Calcular cuántas tareas se deben saltar
        skip = (page - 1) * limit

        # Buscar las tareas aplicando paginación
        tasks = task_collection.find({"user_id": ObjectId(user_id)}).skip(skip).limit(limit)

        # Preparar la lista de tareas en formato JSON
        task_list = [
            {
                "id": str(task["_id"]),
                "title": task["title"],
                "description": task["description"]
            }
            for task in tasks
        ]

        # Estructurar la respuesta con la paginación
        response = {
            "data": task_list,
            "page": page,
            "limit": limit,
            "total": total_tasks
        }

        return util.success_response("Tasks retrieved successfully", response)
