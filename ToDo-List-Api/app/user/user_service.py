import re

class UserService:

    @staticmethod
    # Función para validar el formato de correo electrónico
    def is_valid_email(email):
        # Utilizamos una expresión regular para validar el formato del correo
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)

    @staticmethod
    def validate_fields(name,email,password):
        # Validación de campos
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
    def get_test():
        return "test"

    @staticmethod
    def create_user(name,email,password):

        errors = UserService.validate_fields(name,email,password)
        if errors:
            return {"errors": errors}, 400

        return "hola"
