from app.task.task_controller import task_bp

class TaskModule:
    
    @staticmethod
    def register(app):
        app.register_blueprint(task_bp)
