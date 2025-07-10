from . import dashboard_bp

from models import Feedback
from datetime import datetime, timedelta
from flask import jsonify


@dashboard_bp.get('/data')
def data():
    try:
        today = datetime.now()

        last_15days = today - timedelta(days=15)
        last_30days = today - timedelta(days=30)
        last_60days = today - timedelta(days=60)

        count_15days = Feedback.objects(addedTime__gte=last_15days).count()
        count_30days = Feedback.objects(addedTime__gte=last_30days).count()
        count_60days = Feedback.objects(addedTime__gte=last_60days).count()

        countsData = {
            "last_15days":count_15days,
            "last_30days":count_30days,
            "last_60days":count_60days
        }

        return jsonify({"status":"success", "counts": countsData}),200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error occurred while counting feedback: {str(e)}"
        }), 500