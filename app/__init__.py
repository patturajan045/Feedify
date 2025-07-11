from flask import Flask, session, jsonify
from app.config import Config
from models import *
from mongoengine import connect, connection

def create_App():
    app = Flask(__name__)

    app.config.from_object(Config)

    try:
        connect(host = Config.MONGO_URI)
        if connection.get_connection():
            print("Database Connected Succesfully")

    except Exception as error:
        print(f"connection Failed : {error}")

    from app.role import roleBp
    app.register_blueprint(roleBp, url_prefix = '/role')

    from app.user import userBp
    app.register_blueprint(userBp, url_prefix = '/user') 

    from app.sourcecategory import sourceCategoryBP
    app.register_blueprint(sourceCategoryBP, url_prefix = '/sourcecategory') 

    from app.feedback import feedbackBp
    app.register_blueprint(feedbackBp, url_prefix = '/feedback') 
    
    from app.auth import authBp
    app.register_blueprint(authBp, url_prefix = '/auth')
    
    from app.main import main_bp
    app.register_blueprint(main_bp)
    
    from app.form import formBp
    app.register_blueprint(formBp, url_prefix = '/form') 
   
    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)



    @app.context_processor
    def loadData():
        user = session.get('user')
        print(user)
        if not user:
            print("Not Login")
            return {
                "is_login": False,
                "status": "error", 
                "message": "Please login to continue."
            }

        return {
            "is_login": True,
            "name": user.get('name'),
            "email": user.get('email')
        }
    return app  