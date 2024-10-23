import re
from flask import current_app
from werkzeug.security import generate_password_hash,check_password_hash
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timedelta, timezone
import jwt

class UserService:

    @staticmethod
    def is_valid_email(email):
        # use a regular expression to validate the email format
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)

    @staticmethod
    def validate_fields(name,email,password):
        errors = []

        if not name or not isinstance(name, str):
            errors.append("Name is required and must be a string.")
        
        if not email or not isinstance(email, str):
            errors.append("Email is required and must be a string.")
        elif not UserService.is_valid_email(email):
            errors.append("Invalid email format.")
        
        if not password or not isinstance(password, str):
            errors.append("Password is required and must be a string.")
        elif len(password) < 6:
            errors.append("Password must be at least 6 characters long.")

        
        return errors

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
    def create_user(name,email,password):
        #Validate the input fields
        errors = UserService.validate_fields(name,email,password)
        if errors:
            return {"errors": errors}, 400
        
        #Check if the email already exists in the database
        db = current_app.config['Todo_List_Bd']
        user_collection = db.users  
        existing_user = user_collection.find_one({"email": email})

        if existing_user:
            return {"errors": ["Email already exists"]}, 400

        #Hash the password before storing it
        hashed_password = generate_password_hash(password)

        #Create the user document to insert into MongoDB
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password
        }

        try:
            #Insert the new user into the database
            result = user_collection.insert_one(user_data)
            
            #Generate JWT token after successful registration
            token = UserService.generate_jwt_token(str(result.inserted_id), user_data["email"])

            return {"message": "User created successfully", "token": token}, 201

        except DuplicateKeyError:
            return {"errors": ["Failed to create user, duplicate key error"]}, 500

    @staticmethod
    def login(email,password):
        
        db = current_app.config['Todo_List_Bd']  
        user_collection = db.users  

        #Buscar al usuario por el email
        user = user_collection.find_one({"email": email})

        if not user:
            return {"error": "User not found"}, 404

        #Verificar la contraseña usando check_password_hash
        if not check_password_hash(user["password"], password):
            return {"error": "Invalid password"}, 401

        #Si la autenticación es exitosa, generar un JWT token
        token = UserService.generate_jwt_token(str(user["_id"]), user["email"])

        #Retornar el token en la respuesta
        return {"message": "Login successful", "token": token}, 200
