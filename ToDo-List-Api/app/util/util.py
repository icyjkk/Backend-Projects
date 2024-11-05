from flask import jsonify

class util:

    @staticmethod
    def success_response(message, data=None, status_code=200):
        """
        Generates a successful JSON response.
        
        :param message: Message describing the successful operation.
        :param data: Optional data to include in the response.
        :param status_code: HTTP status code (default is 200).
        :return: Consistent JSON response structure.
        """
        response = {
            "status": "success",
            "message": message
        }

        # Only include the "data" field if it is not None
        if data is not None:
            response["data"] = data

        return jsonify(response), status_code

    @staticmethod
    def error_response(message, errors=None, status_code=400):
        """
        Generates an error JSON response.
        
        :param message: Message describing the error.
        :param errors: Optional details about the error (can be a dict or list).
        :param status_code: HTTP status code (default is 400).
        :return: Consistent JSON response structure with error information.
        """
        response = {
            "status": "error",
            "message": message
        }

        # Only include the "errors" field if it contains valid information
        if errors:
            response["errors"] = errors

        return jsonify(response), status_code
