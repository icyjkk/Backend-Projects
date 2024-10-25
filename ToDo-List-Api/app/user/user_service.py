from flask import current_app
from werkzeug.security import generate_password_hash,check_password_hash
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timedelta, timezone
import jwt
from marshmallow import ValidationError
from app.schemas.schema import UserSchema,LoginSchema
from app.util.util import util

class UserService:

    @staticmethod
    def validate_create_user(request):
        schema = UserSchema()
        try:
            validated_data = schema.load(request.get_json())
            return validated_data, None
        except ValidationError as err:
            return None, util.error_response("Validation failed", err.messages, 400)        
   
    @staticmethod
    def validate_login_data(email, password):
        schema = LoginSchema()
        try:
            data = schema.load({"email": email, "password": password})
            return data, None
        except ValidationError as err:
            return None, util.error_response("Validation failed", err.messages, 400)

    @staticmethod
    def generate_jwt_token(user_id, email):
        
        payload = {
            "user_id": user_id,  
            "email": email,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),  # Token expires in 1 hour
            "iat": datetime.now(timezone.utc)  # Issued at time
        }

        secret_key = current_app.config['JWT_SECRET_KEY']  # Use your secret key from config

        # Generate the JWT token
        token = jwt.encode(payload, secret_key, algorithm='HS256')

        return token

    @staticmethod
    def get_test():
        return "test"

    @staticmethod
    def create_user(data):
        # Validate user data
        validated_data, error_response = UserService.validate_create_user(data)
        if error_response:
            return error_response  # Return error if validation fails

        db = current_app.config['Todo_List_Bd']
        user_collection = db.users

        # Check if the email already exists in the database
        if user_collection.find_one({"email": validated_data["email"]}):
            return util.error_response("Email already exists", None, 400)

        # Hash the password
        hashed_password = generate_password_hash(validated_data["password"])

        # Prepare user data for insertion
        user_data = {
            "name": validated_data["name"],
            "email": validated_data["email"],
            "password": hashed_password
        }

        try:
            result = user_collection.insert_one(user_data)
            token = UserService.generate_jwt_token(str(result.inserted_id), validated_data["email"])
            return util.success_response("User created successfully", {"token": token}, 201)
        except Exception as e:
            return util.error_response("An unexpected error occurred.", {"details": str(e)}, 500)

    @staticmethod
    def login(email,password):
        # Validar los datos de inicio de sesión
        validated_data, validation_error = UserService.validate_login_data(email, password)
        if validation_error:
            return validation_error
        
        db = current_app.config['Todo_List_Bd']  
        user_collection = db.users  

        #Buscar al usuario por el email
        user = user_collection.find_one({"email": validated_data['email']})

        if not user:
            return {"error": "User not found"}, 404

        #Verificar la contraseña usando check_password_hash
        if not check_password_hash(user["password"], validated_data['password']):
            return {"error": "Invalid password"}, 401

        #Si la autenticación es exitosa, generar un JWT token
        token = UserService.generate_jwt_token(str(user["_id"]), user["email"])

        #Retornar el token en la respuesta
        return {"message": "Login successful", "token": token}, 200
