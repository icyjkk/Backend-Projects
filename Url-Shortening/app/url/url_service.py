from flask import current_app
from app.schemas.schema import UrlSchema
from marshmallow import ValidationError
from app.util.util import util
from datetime import datetime
import uuid
import pymongo

class UrlService:

    @staticmethod
    def validate_url(request):
        """Validate the URL."""
        schema = UrlSchema()
        try:
            data = schema.load(request.get_json())
            return data, None
        except ValidationError as err:
            return None, util.error_response("Validation failed", err.messages, 400)

    @staticmethod
    def validate_short_code(short_code):
        """Validate the short code."""
        schema = UrlSchema()
        try:
            # Validar solo el campo short_code
            data = schema.load({"short_code": short_code})
            return data, None
        except ValidationError as err:
            return None, util.error_response("Validation failed", err.messages, 400)

    # Core functions
    @staticmethod
    def get_test():
        """Simple test method to verify service functionality."""
        return "test"
    
    @staticmethod
    def post_shorten(request):
        # Validate url
        validated_data, validation_error = UrlService.validate_url(request)
        if validation_error:
            return validation_error

        # Get database connection
        try:
            db = current_app.config.get('Url_Shortening_Bd')
            if db is None:
                return util.error_response("Database connection error", 500)
            url_collection = db.urls

            # Check if URL already exists
            existing_url = url_collection.find_one({"url": validated_data["url"]})
            if existing_url:
                return util.success_response(
                    "URL already exists",
                    {
                        "id": str(existing_url["_id"]),
                        "url": existing_url["url"],
                        "shortCode": existing_url["shortCode"],
                        "createdAt": existing_url["createdAt"],
                        "updatedAt": existing_url["updatedAt"]
                    },
                    200
                )
        except Exception as e:
            return util.error_response(f"Database connection failed: {str(e)}", 500)
        
        #create short code and check if it already exists
        short_code = str(uuid.uuid4())[:6]
        while url_collection.find_one({"shortCode": short_code}):
            short_code = str(uuid.uuid4())[:6]

        # Create document to insert
        url_doc = {
            "url": validated_data["url"],
            "shortCode": short_code,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
            "accessCount": 0
        }

        # Insert into database
        try:
            result = url_collection.insert_one(url_doc)
        except pymongo.errors.ConnectionFailure:
            return util.error_response("Database connection lost", 500)
        except pymongo.errors.WriteError:
            return util.error_response("Error inserting document", 500)
        except Exception as e:
            return util.error_response(f"Unexpected error: {str(e)}", 500)

        # Prepare the response with the details of the created url
        created_url = {
            "id": str(result.inserted_id),
            "url": validated_data["url"],
            "shortCode": short_code,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }

        # Return the created document
        return util.success_response("URL shortened successfully", created_url, 201)

    @staticmethod
    def get_shorten(short_code):
        # Validate short code
        validated_data, validation_error = UrlService.validate_short_code(short_code)
        if validation_error:
            return validation_error
        
        # Get database connection 
        try:
            db = current_app.config.get('Url_Shortening_Bd')
            if db is None:
                return util.error_response("Database connection error", 500)
            url_collection = db.urls

            # Find URL document by short code
            url_doc = url_collection.find_one({"shortCode": short_code})
            
            # If URL not found, return 404
            if not url_doc:
                return util.error_response("URL not found", status_code=404)
                
            # Increment access count
            url_collection.update_one(
                {"shortCode": short_code},
                {"$inc": {"accessCount": 1}}
            )
                
            # Prepare response with URL details
            url_data = {
                "id": str(url_doc["_id"]),
                "url": url_doc["url"], 
                "shortCode": url_doc["shortCode"],
                "createdAt": url_doc["createdAt"],
                "updatedAt": url_doc["updatedAt"],
            }
            
            return util.success_response("URL found successfully", url_data, 200)

        except Exception as e:
            return util.error_response(f"Database connection failed: {str(e)}", 500)
    
    @staticmethod
    def put_shorten(short_code, request):
        
        # Validate short code
        validated_short_code, validation_error_short_code = UrlService.validate_short_code(short_code)
        validated_url, validation_error_url = UrlService.validate_url(request)
        
        if validation_error_short_code or validation_error_url:
            return validation_error_short_code or validation_error_url
        
        
        # Get database connection 
        try:
            db = current_app.config.get('Url_Shortening_Bd')
            if db is None:
                return util.error_response("Database connection error", 500)
            url_collection = db.urls

            # Find URL document by short code
            url_doc = url_collection.find_one({"shortCode": short_code})
            
            # If URL not found, return 404
            if not url_doc:
                return util.error_response("Short code not found", status_code=404)
                
            # Check if URL already exists
            existing_url = url_collection.find_one({"url": request.get_json()["url"]})
            if existing_url:
                return util.success_response(
                    "URL already exists",
                    {
                        "id": str(existing_url["_id"]),
                        "url": existing_url["url"],
                        "shortCode": existing_url["shortCode"], 
                        "createdAt": existing_url["createdAt"],
                        "updatedAt": existing_url["updatedAt"]
                    },
                    200
                )
                
            # Update URL document and updatedAt timestamp
            url_collection.update_one(
                {"shortCode": short_code}, 
                {
                    "$set": {
                        "url": request.get_json()["url"],
                        "updatedAt": datetime.now().isoformat()
                    }
                }
            )
            
            # Get updated document to return
            updated_url = url_collection.find_one({"shortCode": short_code})
            url_data = {
                "id": str(updated_url["_id"]),
                "url": updated_url["url"],
                "shortCode": updated_url["shortCode"],
                "createdAt": updated_url["createdAt"], 
                "updatedAt": updated_url["updatedAt"]
            }
            
            return util.success_response("URL updated successfully", url_data, 200)

        except Exception as e:
            return util.error_response(f"Database connection failed: {str(e)}", 500)
    
    @staticmethod
    def delete_shorten(short_code):
        # Validate short code
        validated_data, validation_error = UrlService.validate_short_code(short_code)
        if validation_error:
            return validation_error
        
        # Get database connection 
        try:
            db = current_app.config.get('Url_Shortening_Bd')
            if db is None:
                return util.error_response("Database connection error", 500)
            url_collection = db.urls

            # Find URL document by short code
            url_doc = url_collection.find_one({"shortCode": short_code})
            
            # If URL not found, return 404
            if not url_doc:
                return util.error_response("Short code not found", status_code=404)
                
            # Delete URL document
            url_collection.delete_one({"shortCode": short_code})
            
            return util.success_response("Short code deleted successfully", status_code=204)

        except Exception as e:
            return util.error_response(f"Database connection failed: {str(e)}", 500)

    @staticmethod
    def get_stats(short_code):
        # Validate short code
        validated_data, validation_error = UrlService.validate_short_code(short_code)
        if validation_error:
            return validation_error
        
        # Get database connection 
        try:
            db = current_app.config.get('Url_Shortening_Bd')
            if db is None:
                return util.error_response("Database connection error", 500)
            url_collection = db.urls

            # Find URL document by short code
            url_doc = url_collection.find_one({"shortCode": short_code})
            
            # If URL not found, return 404
            if not url_doc:
                return util.error_response("Short code not found", status_code=404)
                
            # Prepare stats data
            stats_data = {
                "id": str(url_doc["_id"]),
                "url": url_doc["url"],
                "shortCode": url_doc["shortCode"],
                "createdAt": url_doc["createdAt"],
                "updatedAt": url_doc["updatedAt"],
                "accessCount": url_doc.get("accessCount", 0)
            }
            
            return util.success_response("Stats retrieved successfully", stats_data, 200)

        except Exception as e:
            return util.error_response(f"Database connection failed: {str(e)}", 500)

