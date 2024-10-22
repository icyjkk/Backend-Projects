from flask import Flask, jsonify
from app.config import Config
from app.user.user_module import UserModule


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register the user module
    UserModule.register(app)

    return app
