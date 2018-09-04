from flask import request, json, Response, Blueprint
from ..models.order import Order

#Bluepring app to handle our order resources
order_api = Blueprint('order', __name__)

@order_api.route('/', methods=['GET'])
def create_ordder():
    """Create order method"""
    return custom_response({'Message': 'Order Created'}, 201)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
