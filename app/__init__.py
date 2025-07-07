from flask import Flask

from app.config import Config

from models import *

from mongoengine import connect,connection

def create_App():
    app = Flask(__name__)

    app.config.from_object(Config)

    try:
        connect(host = Config.MONGO_URI)
        if connection.get_connection():
            app.logger.info("Data Base Connected Succesfully")

    except Exception as error:
        app.logger.error(f"connection Failed:{error}")


    return app  