from app.url.url_controller import url_bp

class UrlModule:
    
    @staticmethod
    def register(app):
        app.register_blueprint(url_bp)
