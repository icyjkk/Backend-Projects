import re
from flask import current_app,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timedelta, timezone
from bson.objectid import ObjectId

class TaskService:

    @staticmethod
    def get_test():
        return "test"

    @staticmethod
    def create_task(user_id,task_title,task_description):

        # Validar los datos de entrada
        if not task_title or not task_description:
            return {"message": "Title and description are required"}, 400

        db = current_app.config['Todo_List_Bd']  # Acceder a la base de datos
        task_collection = db.tasks  # Colección de tareas

        # Crear la tarea
        task_data = {
            "user_id": ObjectId(user_id),
            "title": task_title,
            "description": task_description,
        }

        # Insertar la tarea en la base de datos
        result = task_collection.insert_one(task_data)

        # Preparar la respuesta con los detalles de la tarea creada
        created_task = {
            "id": str(result.inserted_id),
            "title": task_title,
            "description": task_description
        }
        
        return jsonify(created_task), 201
