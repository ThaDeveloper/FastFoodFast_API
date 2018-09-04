from flask import request, jsonify, Response, Blueprint
from ..models.order import Order
from ..models.menu import Menu

#Bluepring app to handle our order resources
order_v1 = Blueprint('order', __name__)
order_inst = Order()
menu_inst = Menu()

@order_v1.route('/', methods=['POST'])
def create_ordder():
    """Create order method"""
    data = request.get_json()
    if not data or not data['items']:
        return jsonify({'Message': 'Order cannot be empty'}, 400)
    price = menu_inst.get_item_price(data['items'])
    order_inst.create_order(
        data['owner'],
        data['items'],
        data['servings'],
        data['servings'] * price,
        data['status'])
    return jsonify({'Message': 'Order Created'}), 201
