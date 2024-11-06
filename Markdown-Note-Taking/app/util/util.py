from flask import jsonify

class util:

    @staticmethod
    def success_response(message, data=None, status_code=200):
        """
        Generates a successful JSON response.
        
        :param message: Message describing the successful operation.
        :param data: Optional data to include in the response.
        :param status_code: HTTP status code (default is 200).
        :return: Consistent JSON response.
        """
        response = {
            "status": "success",
            "message": message
        }

        # Only include the "data" field if it's not None
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
        :return: Consistent JSON response with error information.
        """
        response = {
            "status": "error",
            "message": message
        }

        # Only include the "errors" field if it contains valid information
        if errors:
            response["errors"] = errors

        return jsonify(response), status_code

    @staticmethod
    def simplify_grammar_check_result(result):
        """
        Simplifies the LanguageTool response to return only relevant information.

        :param result: Full response from LanguageTool.
        :return: Dictionary with simplified information.
        """
        simplified_result = {
            "language": result["language"]["name"],
            "detectedLanguage": result["language"]["detectedLanguage"]["name"],
            "matches": []
        }

        for match in result["matches"]:
            simplified_match = {
                "message": match["message"],
                "shortMessage": match.get("shortMessage", ""),
                "offset": match["offset"],
                "length": match["length"],
                "sentence": match["sentence"],
                "replacements": [replacement["value"] for replacement in match["replacements"]],
                "errorType": match["rule"]["issueType"]
            }
            simplified_result["matches"].append(simplified_match)

        return simplified_result

    @staticmethod
    def allowed_file(filename):
        """Checks if the file has an allowed extension (.md)"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'md'
