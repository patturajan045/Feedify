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

    from app.role import roleBp
    app.register_blueprint(roleBp,url_prefix ='/role')

    from app.user import userBp
    app.register_blueprint(userBp,url_prefix ='/user') 

    from app.sourcecategory import sourceCategoryBP
    app.register_blueprint(sourceCategoryBP,url_prefix ='/sourcecategory') 


    from app.feedback import feedbackBp
    app.register_blueprint(feedbackBp,url_prefix ='/feedback') 
    

    from app.auth import authBp
    app.register_blueprint(authBp,url_prefix = '/auth')
    
    from app.main import main_bp
    app.register_blueprint(main_bp)
   


    return app  