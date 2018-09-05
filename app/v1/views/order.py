from flask import request, jsonify, Response, Blueprint
from ..models.order import Order
from ..models.menu import Menu
import datetime

# Bluepring app to handle our order resources
order_v1 = Blueprint('order', __name__)
order_inst = Order()
menu_inst = Menu()


@order_v1.route('', methods=['POST'])
def create_ordder():
    """Create order method"""
    data = request.get_json()
    if not data or not data['items']:
        return jsonify({'Message': 'Order cannot be empty'}), 400
    price = menu_inst.get_item_price(data['items'])
    order_inst.create_order(
        data['owner'],
        data['items'],
        data['servings'],
        data['servings'] * price)
    return jsonify({'Message': 'Order Created'}), 201


@order_v1.route('<int:order_id>', methods=['GET'])
def get_single_order(order_id):
    """Returns a single order"""
    response = order_inst.find_order_by_id(order_id)
    if response:
        return jsonify({"Order": response}), 200
    return jsonify({"Message": "Order not found"}), 404


@order_v1.route('', methods=['GET'])
def get_all_orders():
    """Returns all created orders"""
    return jsonify({"Orders": order_inst.orders}), 200


@order_v1.route('<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Updates the status of a given order"""
    data = request.get_json()
    new_status = data['status']
    new_time = datetime.datetime.now()
    order = order_inst.find_order_by_id(order_id)
    if order:
        response = order_inst.update_order(order_id, new_status,new_time)
        if response:
            return jsonify({'Message': 'Order updated'}), 200
    return jsonify({'Message': 'Order not found'}), 404

@order_v1.route('<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    """Cancels user order and deletes it from the storage"""
    order = order_inst.find_order_by_id(order_id)
    if order:
        order_inst.cancel_order(order_id)
        return jsonify({'Message': 'Order cancelled'}), 200
    return jsonify({'Message': 'Order not found'}), 404