from flask import request, jsonify
from models import User, Role
from . import userBp
from datetime import datetime, timedelta
from mongoengine.queryset.visitor import Q


# Add new data [POST]

@userBp.post('/new')
def addUser():
    data = request.get_json()
    try:
        if data["name"] == " " or data["email"] == " " or data["password"] == " " or data["phone"] == " " or data["role"] == " " :
            return jsonify({"status" : "error", "message" : "Missing Required Field"}), 404
    
        role = data["role"]
        roleId = Role.objects(id = role).first()
        if not roleId:
            return jsonify({"status" : "error", "message" : "Invalid Role Id"})
        
        user = User(
            name = data["name"],
            email = data["email"],
            password = data["password"],
            phone = data["phone"],
            role = roleId
        )
        user.save()
        return jsonify({"status" : "success", "message" : "User Added Successfully"}), 200
    
    except Exception as e:
        return jsonify({f"Error Occured While Using Add User {e}"})
               
        
# Retrieve Specific data [GET]

@userBp.get('/getSpecific')
def getSpecificUser():
    userId = request.args.get("id")
    try:
        user = User.objects(id = userId).first()
        if not user:
            return jsonify({"status" : "error", "message" : "User Not Found"}), 404
        
        userData = {
            "id" : str(user.id),
            "name" : user.name,
            "email" : user.email,
            "phone" : user.phone,
            "password" : user.password,
            "addedTime" : user.addedTime if user.addedTime else None,
            "updatedTime" : user.updatedTime if user.updatedTime else None
        }
        return jsonify({"status" : "success", "data" : userData}), 200
    
    except Exception as e:
        return jsonify({"status" : "error", "message" : f"Error Occured While Retrieving The Specific User : {str(e)}"}), 500  
    
    
# Delete Specific data [DELETE]

@userBp.delete('/deleteSpecific')
def deleteSpecificUser():
    userId = request.args.get("id")
    try:
        user = User.objects(id = userId).first()
        if not user:
            return jsonify({"status" : "error", "message" : "User Not Found"}), 404
        
        user.delete()
        return jsonify({"status" : "success", "message" : "User Deleted Successfully"}), 200
    
    except Exception as e:
        return jsonify({"status" : "error", "message" : f"Error Occured While Delete The Specific User : {str(e)}"}), 500 
    

# Update data [PUT]
    
@userBp.put('/update')
def updateUser():
    userId = request.args.get("id")
    data = request.get_json()
    try:
        user = User.objects(id = userId).first()
        if not user:
            return jsonify({"status" : "error", "message" : "User Not Found"}), 404
        
        if data["name"] == " " or data["email"] == " " or data["password"] == " " or data["phone"] == " " :
            return jsonify({"status" : "error", "message" : "Missing Required Field"}), 404
        
        user.name = data["name"]
        user.email = data["email"]
        user.password = data["password"]
        user.phone = data["phone"]
        role = userId
        user.updatedTime = datetime.now()
        user.save()
        return jsonify({"status" : "success", "message" : "User Updated Successfully"}), 200
    
    except Exception as e:
        return jsonify({"status" : "error", "message" : f"Error Occured While Updating The Specific User : {str(e)}"}), 500 
       
    
# Get all the data [getAll]

@userBp.get('/getAll')
def getAllUser():
    try:
        # Pagination
        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))

        # Search
        search_value = request.args.get('search[value]', '')

        # Sorting
        order_column_index = int(request.args.get('order[0][column]', 0))
        order_direction = request.args.get('order[0][dir]', 'asc')

        # Column mapping
        columns_map = {
            0: None,
            1: 'id',
            2: 'name',
            3: 'email',
            4: 'phone',
            5: 'password',
            3: 'addedTime',
            4: 'updatedTime',
        }

        order_column = columns_map.get(order_column_index)
        order_by = f"-{order_column}" if order_column and order_direction == 'desc' else order_column

        # Base query
        user_query = User.objects()

        # Date filters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        today = request.args.get('today', 'false').lower() == 'true'

        if today:
            user_query = user_query.filter(
                added_time__gte=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            )
        elif start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            user_query = user_query.filter(
                added_time__gte=start_date,
                added_time__lt=end_date
            )

        # Search filter
        if search_value:
            user_query = user_query.filter(
                Q(user_name__icontains=search_value)
            )

        # Counts
        total_user = User.objects.count()
        filtered_user = user_query.count()

        # Sort & paginate
        if order_column:
            user_query = user_query.order_by(order_by)

        user_query = user_query.skip(start).limit(length)

        # Response data
        userData = [{
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "password": user.password,
            "addedTime": user.addedTime,
            "updatedTime": user.updatedTime
        } for user in user_query]

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": total_user,
            "recordsFiltered": filtered_user,
            "data": userData
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error Occurred While Retrieving All User Data: {str(e)}"
        }), 500