from app.user.user_controller import user_bp

class UserModule:
    
    @staticmethod
    def register(app):
        app.register_blueprint(user_bp)
