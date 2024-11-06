from flask import Flask, jsonify
from app.config import Config
from app.note.note_module import NoteModule
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the Limiter
    limiter = Limiter(
        get_remote_address,  
        app=app,
        default_limits=app.config["RATE_LIMITS"]  
    )

    # Add the rate limit error handler
    @app.errorhandler(RateLimitExceeded)
    def rate_limit_handler(e):
        return jsonify(error="Too many requests. Please try again later."), 429


    # Register modules
    NoteModule.register(app)

    return app
