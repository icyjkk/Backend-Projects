from flask import Flask, jsonify
from flask_cors import CORS
from app.config import Config
from app.url.url_module import UrlModule
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
from pymongo import MongoClient
from pymongo.server_api import ServerApi

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})  
    #CORS(app, resources={r"/*": {"origins": ["https://example.com", "https://myapp.com"]}})
    #CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST"]}})


    #Connection MongoDB Atlas
    uri = app.config['MONGO_URI']
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['Url_Shortening_Bd']
    app.config['Url_Shortening_Bd'] = db  # Store Url_Shortening_Bd in app config

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
    UrlModule.register(app)

    return app
