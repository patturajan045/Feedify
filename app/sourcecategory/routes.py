from models import SourceCategory
from datetime import datetime,timedelta
from .import sourceCategoryBP
from flask import request ,jsonify
from mongoengine.queryset.visitor import Q

@sourceCategoryBP.post('/new')
def addSourceCategory():
    data = request.get_json()
    try:
        if data["sourceCategoryname"]=="":
            return jsonify({"status" : "error", "message":"Missing Required Field"}), 404
        
        source = SourceCategory(
            sourceCategoryname = data["sourceCategoryname"]
        )
        source.save()
        return jsonify({"status":"success","message":"Source Added Succesfully"}),200
    except Exception as e:
        return jsonify({
            f"Error Ocuured While Using Add New Source {e}"
        })
    


@sourceCategoryBP.get('/getAll')
def getSourceCategory():
    try:
        # Pagination
        start = int(request.args.get('start', 0))  # Pagination start
        length = int(request.args.get('length', 10))  # Page size
 
        # Search keyword
        search_value = request.args.get('search[value]', '')
 
        # Sorting
        order_column_index = int(request.args.get('order[0][column]', 0))  # Column index to sort
        order_direction = request.args.get('order[0][dir]', 'asc')  # Sort direction: asc or desc
 
        # Map column index to field names
        columns_map = {
            0: None,  # Default (e.g., no sorting)
            1: 'id',
            2: 'sourceCategoryname',
            3: 'addedTime',
            4: 'updatedTime',
        }
 
        # Get sorting column
        order_column = columns_map.get(order_column_index)
        order_by = f"-{order_column}" if order_column and order_direction == 'desc' else order_column
 
        # Initialize query
        source_query = SourceCategory.objects()
 
        # Apply date range filter
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        today = request.args.get('today', 'false').lower() == 'true'
 
        if today:
            source_query = source_query.filter(
                added_time__gte=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            )
        elif start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            source_query = source_query.filter(added_timegte=start_date, added_timelt=end_date)
 
        # Apply search filter (case-insensitive)
        if search_value:
            source_query = source_query.filter(
                Q(sourceCategoryname__icontains=search_value) 
            )
 
        # Total and filtered counts
        total_source = SourceCategory.objects.count()
        filtered_source = source_query.count()
 
        # Apply sorting and pagination
        if order_column:
            source_query = source_query.order_by(order_by)
        source_query = source_query.skip(start).limit(length)
 
        # Prepare response data using list comprehension
        sourceData = [{
          "id": str(source.id),
          "sourceCategoryname": source.sourceCategoryname,
          "addedTime": source.addedTime if source.addedTime else None,
          "updatedTime": source.updatedTime if source.updatedTime else None
        } for source in source_query]
 
        # Return data in DataTables format
        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": total_source,
            "recordsFiltered": filtered_source,
            "data": sourceData
        }), 200
    
    except Exception as e:
        return jsonify({"status":"error", "message":f"Error Occured While Retrieving All Source Data {e}"}) 
    


@sourceCategoryBP.get('/getSpecific')
def getSpecificSourrceCategory():
    sourceId = request.args.get("id")
    try:
        source = SourceCategory.objects(id = sourceId).first()
        if not source:
            return jsonify({"status" : "error", "message" : "SourceCategory Not Found"}), 404
        
        sourceData = {
            "id" : str(source.id),
            "sourceCategoryname" : source.sourceCategoryname,
            "addedTime" : source.addedTime if source.addedTime else None,
            "updatedTime" : source.updatedTime if source.updatedTime else None
        }
        return jsonify({"status" : "success", "data" : sourceData}), 200
    
    except Exception as e:
        return jsonify({"status" : "error", "message" : f"Error Occured While Retrieving The Specific Source : {str(e)}"}),500
    
@sourceCategoryBP.delete('/deleteSpecific')
def deleteSpecificSourceCategory():
    sourceId = request.args.get("id")
    try:
        source = SourceCategory.objects(id = sourceId).first()
        if not source:
            return jsonify({"status" : "error", "message" : "SourceCategory Not Found"}), 404
        
        source.delete()
        return jsonify({"status" : "success", "message" : "SourceCategory Deleted Successfully"}), 200
    
    except Exception as e:
        return jsonify({"status" : "error", "message" : f"Error Occured While Delete The Specific Source : {str(e)}"}),500
       

@sourceCategoryBP.put('/update')
def updateSourceCategory():
    sourceId = request.args.get("id")
    data = request.get_json()
    try:
        source = SourceCategory.objects(id = sourceId).first()
        if not source:
            return jsonify({"status" : "error", "message" : "SourceCategory Not Found"}), 404
        
        if data["sourceCategoryname"] == " ":
            return jsonify({"status" : "error", "message" : "Missing Required Field"}), 404
        
        source.sourceCategoryname = data["sourceCategoryname"]
        source.updatedTime = datetime.now()
        source.save()
        return jsonify({"status" : "success", "message" : "SourceCategory Updated Successfully"}), 200
    
    except Exception as e:
        return jsonify({"status" : "error", "message" : f"Error Occured While Updating The Specific Source : {str(e)}"}),500
          
     
             
                  
            

