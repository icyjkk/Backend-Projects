from flask import jsonify

class util:

    @staticmethod
    def success_response(message, data=None, status_code=200):
        """
        Genera una respuesta de éxito en formato JSON.
        
        :param message: Mensaje que describe la operación exitosa.
        :param data: Datos opcionales que se devolverán en la respuesta.
        :param status_code: Código de estado HTTP (por defecto es 200).
        :return: Respuesta JSON con estructura consistente.
        """
        response = {
            "status": "success",
            "message": message
        }

        # Solo incluir el campo "data" si no es None
        if data is not None:
            response["data"] = data

        return jsonify(response), status_code

    @staticmethod
    def error_response(message, errors=None, status_code=400):
        """
        Genera una respuesta de error en formato JSON.
        
        :param message: Mensaje que describe el error.
        :param errors: Detalles opcionales sobre el error (puede ser un dict o lista).
        :param status_code: Código de estado HTTP (por defecto es 400).
        :return: Respuesta JSON con estructura consistente.
        """
        response = {
            "status": "error",
            "message": message
        }

        # Solo incluir el campo "errors" si contiene información válida
        if errors:
            response["errors"] = errors

        return jsonify(response), status_code
