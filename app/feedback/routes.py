from models import Feedback,SourceCategory
from datetime import datetime,timedelta
from .import feedbackBp
from flask import request ,jsonify
from mongoengine.queryset.visitor import Q

@feedbackBp.post('/new')
def addFeedback():
    data = request.get_json()
    try:
        if data["feedbackName"]=="" or data["feedbackData"]=="" or data["rating"]=="" or data["status"]=="" or data["SourceCategory"]:
            return jsonify({"status" : "error", "message":"Missing Required Field"}), 404
        
        sourcecategory=data=["sourcecategory"]
        sourceId=SourceCategory.objects(id=sourcecategory).first()
        
        if not sourceId:
            return jsonify({"status":"error" , "message":" Invalid SourceId"})
        
        feedback= Feedback(
            feedbackName = data["feedback feedbackName"],
            sourceCategory=data["Sourcecategory"],
            feedbackData=data["feedbackData"],
            rating=data["rating"],
            status=data["status"]
        )
        feedback.save()
        return jsonify({"status":"success","message":"Feedback Added Successfully"}),200
    except Exception as e:
        return jsonify({
            f"Error Ocuured While Using Add New Feedback {e}"
        })
    

@feedbackBp.get('/getAll')
def getFeedback():
    try:
        # Pagination
        start = int(request.args.get('start', 0))  # Pagination start
        length = int(request.args.get('length', 10))  # Page size
 
        # Search keyword
        search_value = request.args.get('search[value]', '')
 
        # Sorting
        order_column_index = int(request.args.get('order[0][column]', 0))  # Column index to sort
        order_direction = request.args.get('order[0][dir]', 'asc')  # Sort direction: asc or desc
 
        # Map column index to field  feedbackNames
        columns_map = {
            0: None,  # Default (e.g., no sorting)
            1: 'id',
            2: 'feedbackName',
            3: 'SourceCategory',
            4: 'feedbackData',
            5: 'rating',
            6: 'status',
            7: 'addedTime',
            8: 'updatedTime',
        }
 
        # Get sorting column
        order_column = columns_map.get(order_column_index)
        order_by = f"-{order_column}" if order_column and order_direction == 'desc' else order_column
 
        # Initialize query
        feedback_query = Feedback.objects()
 
        # Apply date range filter
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        today = request.args.get('today', 'false').lower() == 'true'
 
        if today:
            feedback_query = feedback_query.filter(
                added_time__gte=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            )
        elif start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            feedback_query = feedback_query.filter(added_timegte=start_date, added_timelt=end_date)
 
        # Apply search filter (case-insensitive)
        if search_value:
            feedback_query = feedback_query.filter(
                Q( feedbackName__icontains=search_value) |
                Q(status__icontains=search_value)
            )
 
        # Total and filtered counts
        total_feedback= Feedback.objects.count()
        filtered_feedback = feedback_query.count()
 
        # Apply sorting and pagination
        if order_column:
            feedback_query = feedback_query.order_by(order_by)
        feedback_query = feedback_query.skip(start).limit(length)
 
        # Prepare response data using list comprehension
        feedbackData = [{
          "id": str(feedback.id),
          "feedbackName": feedback.feedbackName,
          "feedbackData": feedback.feedbackData,
          "sourceCategory":feedback.sourceCategory,
          "rating": feedback.rating,
          "status": feedback.status,
          "addedTime": feedback.addedTime if feedback.addedTime else None,
          "updatedTime": feedback.updatedTime if feedback.updatedTime else None
        } for feedback in feedback_query]
 
        # Return data in DataTables format
        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": total_feedback,
            "recordsFiltered": filtered_feedback,
            "data": feedbackData
        }), 200
    
    except Exception as e:
        return jsonify({"status":"error", "message":f"Error Occured While Retrieving All Feedback Data {e}"}) 
    

@feedbackBp.get('/getSpecific')
def getSpecificfeedback():
    feedbackId = request.args.get("id")
    try:
        feedback = Feedback.objects(id = feedbackId).first()
        if not feedback:
            return jsonify({"Status" : "error", "message" : "Feedback Not Found"}), 404
        
        feedbackData = {
            "id" : str(feedback.id),
            "feedbackName" : feedback.feedbackName,
            "feedbackData" : feedback.feedbackData,
            "sourceCategory":feedback.sourceCategory,
            "rating" : feedback.rating,
            "status" : feedback.status,
            "addedTime" : feedback.addedTime if feedback.addedTime else None,
            "updatedTime" : feedback.updatedTime if feedback.updatedTime else None
        }
        return jsonify({"status" : "success", "data" : feedbackData}), 200
    
    except Exception as e:
        return jsonify({"status" : "error", "message" : f"Error Occured While Retrieving The Specific Feedback : {str(e)}"}),500
    

@feedbackBp.delete('/deleteSpecific')
def deleteSpecificfeedback():
    feedbackId = request.args.get("id")
    try:
        feedback = feedback.objects(id = feedbackId).first()
        if not feedback:
            return jsonify({"status" : "error", "message" : "Feedback Not Found"}), 404
        
        feedback.delete()
        return jsonify({"status" : "success", "message" : "Feedback Deleted Successfully"}), 200
    
    except Exception as e:
        return jsonify({"status" : "error", "message" : f"Error Occured While Delete The Specific Feedback : {str(e)}"}),500
       
@feedbackBp.put('/update')
def updatefeedback():
    feedbackId = request.args.get("id")
    data = request.get_json()
    try:
        feedback = feedback.objects(id = feedbackId).first()
        if not feedback:
            return jsonify({"status" : "error", "message" : "Feedback Not Found"}), 404
        
        if data["feedbackName"]=="" or data["feedbackData"]=="" or data["rating"]=="" or data["status"]=="" or data["SourceCategory"]:
            return jsonify({"status" : "error", "message":"missing Required Field"}), 404
        
        sourcecategory=data=["SourceCategory"]
        sourceId=SourceCategory.objects(id=sourcecategory).first()
        
        if not sourceId:
            return jsonify({"status":"error" , "message":" Invalid SourceId"})
        
        feedback.feedbackName = data[" feedbackName"]
        feedback.feedbackData =data["feedbackData"]
        feedback.rating = data["rating"]
        feedback.status=data["status"]
        feedback.sourceCategory = sourceId
        feedback.updatedTime = datetime.now()
        feedback.save()
        return jsonify({"status" : "success", "message" : "Feedback Updated Successfully"}), 200
    
    except Exception as e:
        return jsonify({"status" : "error", "message" : f"Error occured while updating the specific feedback : {str(e)}"}),500
          
     



                  
            

