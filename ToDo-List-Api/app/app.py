from flask import Flask, jsonify
from app.config import Config
from app.user.user_module import UserModule
from app.task.task_module import TaskModule
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    #Connection MongoDB Atlas
    uri = app.config['MONGO_URI']
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['Todo_List_Bd']
    app.config['Todo_List_Bd'] = db  # Store Todo_List_Bd in app config

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
    UserModule.register(app)
    TaskModule.register(app)

    return app
