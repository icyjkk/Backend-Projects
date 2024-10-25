from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
import jwt
from marshmallow import ValidationError
from app.schemas.schema import UserSchema, LoginSchema
from app.util.util import util

class UserService:

    @staticmethod
    def validate_create_user(request):
        """Validate user registration data using UserSchema."""
        schema = UserSchema()
        try:
            validated_data = schema.load(request.get_json())
            return validated_data, None
        except ValidationError as err:
            return None, util.error_response("Validation failed", err.messages, 400)        

    @staticmethod
    def validate_login_data(email, password):
        """Validate login data using LoginSchema."""
        schema = LoginSchema()
        try:
            data = schema.load({"email": email, "password": password})
            return data, None
        except ValidationError as err:
            return None, util.error_response("Validation failed", err.messages, 400)

    @staticmethod
    def generate_jwt_token(user_id, email):
        """Generate JWT access token with a 1-hour expiration."""
        payload = {
            "user_id": user_id,  
            "email": email,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),  # Token expires in 1 hour
            "iat": datetime.now(timezone.utc)  # Issued at time
        }

        # Retrieve secret key from the app configuration
        secret_key = current_app.config['JWT_SECRET_KEY']

        # Generate the JWT token
        token = jwt.encode(payload, secret_key, algorithm='HS256')

        return token

    @staticmethod
    def get_test():
        """Simple test method to verify service functionality."""
        return "test"

    @staticmethod
    def create_user(data):
        """Create a new user, validate data, hash password, and store in database."""
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
            # Insert the new user into the database
            result = user_collection.insert_one(user_data)
            
            # Generate JWT token upon successful registration
            token = UserService.generate_jwt_token(str(result.inserted_id), validated_data["email"])
            return util.success_response("User created successfully", {"token": token}, 201)
        except Exception as e:
            # Handle unexpected errors during database insertion
            return util.error_response("An unexpected error occurred.", {"details": str(e)}, 500)

    @staticmethod
    def login(email, password):
        """Authenticate user, validate credentials, and return access token."""
        # Validate login data
        validated_data, validation_error = UserService.validate_login_data(email, password)
        if validation_error:
            return validation_error
        
        db = current_app.config['Todo_List_Bd']  
        user_collection = db.users  

        # Find the user by email in the database
        user = user_collection.find_one({"email": validated_data['email']})

        if not user:
            # Return error if user is not found
            return util.error_response("User not found", None, 404)

        # Verify password using check_password_hash
        if not check_password_hash(user["password"], validated_data['password']):
            # Return error if password is incorrect
            return util.error_response("Invalid password", None, 401)

        # Generate JWT token upon successful authentication
        token = UserService.generate_jwt_token(str(user["_id"]), user["email"])

        # Return token and success message
        return util.success_response("Login successful", {"token": token}, 200)
