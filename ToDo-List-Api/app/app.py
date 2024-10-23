from flask import Flask, jsonify
from app.config import Config
from app.user.user_module import UserModule
from app.task.task_module import TaskModule
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    #Connection MongoDB Atlas
    uri = f'mongodb+srv://icyjkk:{app.config["MONGO_KEY"]}@cluster0-backend-projec.9ms0b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0-Backend-projects'
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['Todo_List_Bd']
    app.config['Todo_List_Bd'] = db  # Store Todo_List_Bd in app config



    # Register modules
    UserModule.register(app)
    TaskModule.register(app)

    return app
