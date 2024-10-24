import jwt
from functools import wraps
from flask import request, jsonify, current_app
from app.util.util import util

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Verificar si el token está en el header Authorization
        if 'Authorization' in request.headers:
            try:
                # Intentar extraer el token del encabezado Authorization
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                # Si el encabezado Authorization está mal formado
                return util.error_response("Authorization header is malformed", None, 401)

        # Si no se ha proporcionado token
        if not token:
            return util.error_response("Token is missing", status_code=401)

        try:
            # Decodificar el token JWT para obtener el user_id
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            user_id = data['user_id']  # Extraer el user_id del token
        except jwt.ExpiredSignatureError:
            # Error cuando el token ha expirado
            return util.error_response("Token has expired", status_code=401)
        except jwt.InvalidTokenError:
            # Error cuando el token es inválido
            return util.error_response("Invalid token", status_code=401)
        except Exception as e:
            # Cualquier otro error relacionado con el token
            return util.error_response("Token is invalid", status_code=401)

        # Continuar con la función original pasando el user_id
        return f(user_id, *args, **kwargs)

    return decorated
