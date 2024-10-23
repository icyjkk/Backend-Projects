import jwt
from functools import wraps
from flask import request, jsonify, current_app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Verificar si el token está en el header Authorization
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
            
        if not token:
            return jsonify({'message': 'Unauthorized'}), 401

        try:
            # Decodificar el token para obtener el user_id
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            user_id = data['user_id']  # Extraer el user_id del token
        except Exception as e:
            return jsonify({'message': 'Unauthorized'}), 401

        return f(user_id, *args, **kwargs)
    return decorated
