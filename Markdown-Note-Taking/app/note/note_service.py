from flask import current_app
from app.util.util import util
import markdown
from bs4 import BeautifulSoup
import requests
import uuid
from datetime import datetime
from flask import request, jsonify
from werkzeug.utils import secure_filename
import json
import os
from app.schemas.schema import NoteSchema
from marshmallow import ValidationError


class NoteService:

    @staticmethod
    def validate_note(request):
        """Validates the note text using the schema."""
        schema = NoteSchema()
        try:
            data = schema.load(request.get_json())
            return data, None
        except ValidationError as err:
            return None, util.error_response("Validation failed", err.messages, 400)

    @staticmethod
    def save_note_to_file(note):
        """Saves the note in notes.json file."""
        if os.path.exists("notes.json"):
            with open("notes.json", "r", encoding="utf-8") as file:
                notes = json.load(file)
        else:
            notes = []

        notes.append(note)
        
        with open("notes.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)   

    # Core functions

    @staticmethod
    def post_check_grammar(request):
        """
        Checks the grammar of the provided note content using LanguageTool API.
        
        :param request: Flask request object containing the note text and language.
        :return: JSON response with grammar check results or error message.
        """
        # Validate the note text
        validated_data, validation_error = NoteService.validate_note(request)

        if validation_error:
            return validation_error
        
        # Convert Markdown to HTML
        html_content = markdown.markdown(validated_data.get("note"))

        # Use BeautifulSoup to extract plain text only
        soup = BeautifulSoup(html_content, "html.parser")
        plain_text = soup.get_text()

        # Define the URL for the LanguageTool API
        url = "https://api.languagetool.org/v2/check"
        params = {
            "text": plain_text,
            "language": validated_data.get("language")  
        }

        # Send request to LanguageTool API
        response = requests.post(url, data=params)
        
        # Handle LanguageTool response
        if response.status_code == 200:
            full_result = response.json()
            # Process the result to extract only relevant data
            simplified_result = util.simplify_grammar_check_result(full_result)
            # Return success response with simplified data
            return util.success_response(
                message="Grammar check completed successfully",
                data=simplified_result,
                status_code=200
            )
        else:
            # Return error response if LanguageTool fails
            return util.error_response(
                message="Error in grammar check service",
                errors={"status_code": response.status_code, "detail": response.text},
                status_code=500
            )
        
    @staticmethod
    def post_save_note(request):
        """
        Saves a new note provided as a file or Markdown text.
        
        :param request: Flask request object containing the file or text content.
        :return: JSON response confirming the note was saved or an error message.
        """
        # Check if a file has been provided
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return util.error_response(
                    message="No file selected",
                    errors={"file": ["File is required"]},
                    status_code=400
                )
            if not util.allowed_file(file.filename):
                return util.error_response(
                    message="Invalid file type. Only .md files are allowed.",
                    errors={"file": ["Invalid file type"]},
                    status_code=400
                )

            # Process the file and save its content
            filename = secure_filename(file.filename)  # Clean and secure the file name before saving.
            file_content = file.read().decode("utf-8")
            note_id = str(uuid.uuid4())
            note = {
                "id": note_id,
                "filename": filename,
                "content": file_content,
                "created_at": datetime.now().isoformat()
            }

        # Check if Markdown text has been provided
        elif 'text' in request.form:
            text = request.form['text']
            if not text.strip():
                return util.error_response(
                    message="Text is required and cannot be empty",
                    errors={"text": ["Text cannot be empty"]},
                    status_code=400
                )

            # Decode text if it's escaped to avoid duplications
            try:
                text = json.loads(f'"{text}"')  # Removes double escaping
            except json.JSONDecodeError:
                pass  # If it fails, continue with the original text

            note_id = str(uuid.uuid4())
            note = {
                "id": note_id,
                "filename": "markdown_text.md",
                "content": text,
                "created_at": datetime.now().isoformat()
            }

        else:
            return util.error_response(
                message="No file or text provided",
                errors={"input": ["Either 'file' or 'text' must be provided"]},
                status_code=400
            )

        # Save the note in notes.json
        NoteService.save_note_to_file(note)
        return util.success_response(
            message="Note saved successfully",
            data={"id": note_id, "filename": note["filename"]},
            status_code=201
        )

    @staticmethod
    def get_list_notes():
        """Reads notes from notes.json and returns them in the response."""
        try:
            with open("notes.json", "r", encoding="utf-8") as file:
                notes = json.load(file)
        except FileNotFoundError:
            # Return an empty list if the file does not exist
            notes = []

        return util.success_response(
            message="List of notes retrieved successfully",
            data=notes,
            status_code=200
        )

    @staticmethod
    def get_html_note(note_id):
        """Returns the HTML of a note specified by its ID."""
        try:
            with open("notes.json", "r", encoding="utf-8") as file:
                notes = json.load(file)
        except FileNotFoundError:
            return util.error_response(
                message="There are no notes",
                status_code=404
            )

        # Search for the note by ID
        note = next((note for note in notes if note['id'] == note_id), None)

        if note is None:
            return util.error_response(
                message="Note not found",
                status_code=404
            )

        # Render the Markdown content to HTML
        html_content = markdown.markdown(note['content'])

        return html_content

    @staticmethod
    def get_test():
        """Simple test method to verify service functionality."""
        return "test"
