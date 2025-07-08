from flask import request, jsonify
from models import Role
from . import roleBp
from datetime import datetime,timedelta
from mongoengine.queryset.visitor import Q

#POST

@roleBp.post('/new')
def addRole():
    data = request.get_json()
    try:
        if data["name"] == " ":
            return jsonify({"status": "Error", "message": "Missing Required Field"}),404 
        role = Role(
            name= data["name"]      
        )
        role.save()
        return jsonify({"status: Success" , "message:Role added Successfully"}),200 
    except Exception as e:
        return jsonify({f"Error Occured While Using Add Role{e}"})
    
    
#GET

@roleBp.post('/getSpecific')
def getSpecificRole():
    roleId = request.args.get("id")
    try:
        role = Role.objects(id=roleId).first()
        if not role:
            return jsonify({"status":"Error" , "message": "Role Not Found"}),404
        roleData = {
            "id":str(role.id),
            "name": role.name,
            "addedTime":role.addedTime if role.addedTime else None,
            "updatedTime":role.updatedTime if role.updatedTime else None
        }  
        return jsonify({"status":"Success","data": roleData}),200
    except Exception as e:
        return jsonify({"status":"Error","message":f"Error Occured While Retrieving The Specific Role:{str(e)}"}),500
    
#delete  
   
@roleBp.delete('/deleteSpecific')
def deleteSpecificRole():
    roleId = request.args.get('id')
    try:
        role=Role.objects(id=roleId).first()   
        if not role:
            return jsonify({"status":"error","message":"Role not found"}),404
        role.delete()
        return jsonify({"status":"Success","message":"role deleted successfully"}),200
    except Exception as e:
        return jsonify({"status":"error","message":f"Error occured while retriving the specific role:{str(e)}"}),500
    
#update

@roleBp.put('/update')
def updateRole():
    roleId=request.args.get('id')
    data=request.get_json()
    try:
        role=Role.objects(id=roleId).first()  
        if not role:
            return jsonify({"status":"error","message":"Role not found"}),404
        if data["name"]=="":
          return jsonify({"status":"Success","message":"Missing Required field"}),404
        role.name =data["name"]
        role.updatedTime =datetime.now()
        role.save()
        return jsonify({"status":"success","message":"role updated successfully"}),200
    except Exception as e:
        return jsonify({"status":"error","message":f"Error occured while retriving the specific role:{str(e)}"}),500
    
    
    
# Get all the data [getAll]

@roleBp.get('/getAll')
def getAllRole():
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
            3: 'addedTime',
            4: 'updatedTime'
        }

        order_column = columns_map.get(order_column_index)
        order_by = f"-{order_column}" if order_column and order_direction == 'desc' else order_column

        # Base query
        role_query = Role.objects()

        # Date filters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        today = request.args.get('today', 'false').lower() == 'true'

        if today:
            role_query = role_query.filter(
                added_time__gte=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            )
        elif start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            role_query = role_query.filter(
                added_time__gte=start_date,
                added_time__lt=end_date
            )

        # Search filter
        if search_value:
            role_query = role_query.filter(
                Q(role_name__icontains=search_value)
            )

        # Counts
        total_role = Role.objects.count()
        filtered_role = role_query.count()

        # Sort & paginate
        if order_column:
            role_query = role_query.order_by(order_by)

        role_query = role_query.skip(start).limit(length)

        # Response data
        roleData = [{
            "id": str(role.id),
            "name": role.name,
            "addedTime": role.addedTime,
            "updatedTime": role.updatedTime
        } for role in role_query]

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": total_role,
            "recordsFiltered": filtered_role,
            "data": roleData
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error occurred while retrieving all role data: {str(e)}"}),500      
     
   
    
    

    
            
