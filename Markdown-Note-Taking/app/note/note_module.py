from app.note.note_controller import note_bp

class NoteModule:
    
    @staticmethod
    def register(app):
        app.register_blueprint(note_bp)
