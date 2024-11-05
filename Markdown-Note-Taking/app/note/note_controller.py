from flask import Blueprint, request, jsonify, current_app
from app.note.note_service import NoteService

# Define the 'note' blueprint with a URL prefix '/note'
note_bp = Blueprint('note', __name__, url_prefix='/note')

@note_bp.route('/check-grammar', methods=['POST'])
def post_check_grammar():
    """Endpoint to check the grammar of the provided note content."""
    return NoteService.post_check_grammar(request)

@note_bp.route('/save-note', methods=['POST'])
def post_save_note():
    """Endpoint to save a new note. Accepts file or Markdown text."""
    return NoteService.post_save_note(request)

@note_bp.route('/list-notes', methods=['GET'])
def get_list_notes():
    """Endpoint to retrieve a list of all saved notes."""
    return NoteService.get_list_notes()

@note_bp.route('/render-note/<note_id>', methods=['GET'])
def get_html_note(note_id):
    """Endpoint to render a specific note as HTML, identified by note_id."""
    return NoteService.get_html_note(note_id)

@note_bp.route('/test', methods=['GET'])
def get_test():
    """Simple endpoint to verify service functionality."""
    return NoteService.get_test()
