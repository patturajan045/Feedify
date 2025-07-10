from flask import request, jsonify
from models import Form, SourceCategory
from . import formBp
from datetime import datetime, timedelta
from mongoengine.queryset.visitor import Q


# Add new data [POST]

@formBp.post('/new')
def addForm():
    data = request.get_json()
    try:
        if data["name"] == " " or data["description"] == " " or data["inputs"] == " " or data["sourceCategory"] == " " :
            return jsonify({"status" : "error", "message" : "Missing Required Field"}), 404
    
        sourceCategory = data["sourceCategory"]
        sourceCategoryId = SourceCategory.objects(id = sourceCategory).first()
        if not sourceCategoryId:
            return jsonify({"status" : "error", "message" : "Invalid sourceCategory Id"})
        
        form = Form(
            name = data["name"],
            description = data["description"],
            inputs = data["inputs"],
            sourceCategory = sourceCategoryId
        )
        form.save()
        return jsonify({"status" : "success", "message" : "Form Created Successfully"}), 200
    
    except Exception as e:
        return jsonify({f"Error Occured While Using Add Form {e}"})
               
        
# Retrieve Specific data [GET]

@formBp.get('/getSpecific')
def getSpecificForm():
    formId = request.args.get("id")
    try:
        form = Form.objects(id = formId).first()
        if not form:
            return jsonify({"status" : "error", "message" : "Form Not Found"}), 404
        
        formData = {
            "id" : str(form.id),
            "name" : form.name,
            "description" : form.description,
            "inputs" : form.inputs,
            "addedTime" : form.addedTime if form.addedTime else None,
            "updatedTime" : form.updatedTime if form.updatedTime else None
        }
        return jsonify({"status" : "success", "data" : formData}), 200
    
    except Exception as e:
        return jsonify({"status" : "error", "message" : f"Error Occured While Retrieving The Specific Form : {str(e)}"}), 500  
    
    
# Delete Specific data [DELETE]

@formBp.delete('/deleteSpecific')
def deleteSpecificForm():
    formId = request.args.get("id")
    try:
        form = Form.objects(id = formId).first()
        if not form:
            return jsonify({"status" : "error", "message" : "Form Not Found"}), 404
        
        form.delete()
        return jsonify({"status" : "success", "message" : "Form Deleted Successfully"}), 200
    
    except Exception as e:
        return jsonify({"status" : "error", "message" : f"Error Occured While Delete The Specific Form : {str(e)}"}), 500 
    

# Update data [PUT]
    
@formBp.put('/update')
def updateForm():
    formId = request.args.get("id")
    data = request.get_json()
    try:
        form = Form.objects(id = formId).first()
        if not form:
            return jsonify({"status" : "error", "message" : "Form Not Found"}), 404
        
        if data["name"] == " " or data["description"] == " " or data["inputs"] == " " or data["sourceCategory"] == " " :
            return jsonify({"status" : "error", "message" : "Missing Required Field"}), 404
        
        sourceCategory = data["sourceCategory"]
        sourceCategoryId = SourceCategory.objects(id = sourceCategory).first()
        if not sourceCategoryId:
            return jsonify({"status" : "error", "message" : "Invalid sourceCategory Id"})
        
        form.name = data["name"]
        form.description = data["description"]
        form.inputs = data["inputs"]
        form.sourceCategory = sourceCategoryId
        form.updatedTime = datetime.now()
        form.save()
        return jsonify({"status" : "success", "message" : "Form Updated Successfully"}), 200
    
    except Exception as e:
        return jsonify({"status" : "error", "message" : f"Error Occured While Updating The Specific Form : {str(e)}"}), 500 
       
    
# Get all the data [getAll]

@formBp.get('/getAll')
def getAllForm():
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
            3: 'description',
            4: 'inputs',
            5: 'addedTime',
            6: 'updatedTime',
        }

        order_column = columns_map.get(order_column_index)
        order_by = f"-{order_column}" if order_column and order_direction == 'desc' else order_column

        # Base query
        form_query = Form.objects()

        # Date filters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        today = request.args.get('today', 'false').lower() == 'true'

        if today:
            form_query = form_query.filter(
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
            form_query = form_query.filter(
                Q(name__icontains=search_value)
            )

        # Counts
        total_form = Form.objects.count()
        filtered_form = form_query.count()

        # Sort & paginate
        if order_column:
            form_query = form_query.order_by(order_by)

        form_query = form_query.skip(start).limit(length)

        # Response data
        formData = [{
            "id": str(form.id),
            "name": form.name,
            "description": form.description,
            "inputs": form.inputs,
            "addedTime": form.addedTime,
            "updatedTime": form.updatedTime
        } for form in form_query]

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": total_form,
            "recordsFiltered": filtered_form,
            "data": formData
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error Occurred While Retrieving All Form Data: {str(e)}"
        }), 500