from models import User,Role
from  flask import request, jsonify, session, redirect
from datetime import datetime 
from . import authBp


@authBp.post('/register')
def register():
    data = request.get_json()
    print(data)
    try:
        if data["name"] == "" or data["email"] == "" or data["password"] == "" or data["phone"] == "":
            return jsonify({"status" : "error", "message" : "Missing Required Field"}), 404
        
        role = Role.objects(name="user").first()
        if not role:
            return jsonify({"status":"error", "message":" Invalid Role"})
        

        user = User(
            name = data["name"],
            email = data["email"],
            password = data["password"],
            phone = data["phone"],
            role=role
        ).save()

        session["user"] = {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }

        return jsonify({"status" : "success", "message" : "Register Successfully"}), 200
    
    except Exception as e:
        return jsonify({f"Error Occured While Using Register{e}"})
    

@authBp.post('/login')
def login():
    data = request.get_json()
    try:
        if data["email"] == "" or data["password"] == "" :
            return jsonify({"status" : "error", "message" : "Missing Required Field"}), 404
        
        user = User.objects(email = data["email"]).first()
        if not user:
            return jsonify({"status" : "error", "message" : "User Not Found"}), 404
        
        if user.password != data["password"]:
            return jsonify({"status":"succes","message":"User Found, But Password Is Not Matched"})
        

        session["user"] = {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        
        return jsonify({"status" : "success", "message" : "Login Successfully"}), 200

    except Exception as e:
        return jsonify({f"Error Occured While Using Login {e}"})
        
        
@authBp.get('/logout')
def logout():
    if session["user"]:
        session.clear()
        return redirect('/login')
    else:
        return jsonify({"status": "error", "message": "You are not logged in. Please login to continue."})