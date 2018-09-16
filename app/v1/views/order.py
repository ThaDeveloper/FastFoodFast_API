from flask import request, jsonify, Response, Blueprint
import datetime

from ..models.order import Order
from ..models.menu import Menu
from ...shared.authentication import Auth
from ...shared.validation import ValidationError

# Bluepring app to handle our order resources
order_v1 = Blueprint('order', __name__)
order_inst = Order()
all_orders = order_inst.orders
menu_inst = Menu()


@order_v1.route('', methods=['POST'])
@Auth.token_required
def create_order(current_user):
    """Create order method"""
    data = request.get_json()
    try:
        sanitized = order_inst.import_data(data)
        if sanitized == "Invalid":
            return jsonify({'Message': 'Order cannot be empty'}), 400
    except ValidationError as e:
        return jsonify({"Message": str(e)}), 400

    user = current_user['username']
    total = order_inst.total_cost(data['items'])
    order_inst.create_order(
        user,
        data['items'],
        total)
    return jsonify({'Message': 'Order Created'}), 201


@order_v1.route('<int:order_id>', methods=['GET'])
@Auth.token_required
def get_single_order(current_user, order_id):
    """Returns a single order for the owner or admin"""
    order = order_inst.find_order_by_id(order_id)
    print(current_user)
    if order:
        if current_user['username'] == order['user_id']:
            return jsonify({"Order": order}), 200
        return jsonify({"Message": "Not authorized to view order"}), 401

    return jsonify({"Message": "Order not found"}), 404


@order_v1.route('', methods=['GET'])
@Auth.token_required
def get_all_orders(current_user):
    """Returns all created orders"""
    if not all_orders:
        return jsonify({'Message': "No orders found"}), 200
    return jsonify({"Orders": all_orders}), 200

@order_v1.route('/customer', methods=['GET'])
@Auth.token_required
def get_order_history(current_user):
    """Returns all orders user made in the past"""
    user_orders = []
    for order in all_orders:
        if all_orders[order]['user_id'] == current_user['username']:
            user_orders.append(all_orders[order])
    if user_orders:
        return jsonify({"Your orders": user_orders}), 200
    return jsonify({"Message": "You have 0 orders"}), 200


@order_v1.route('<int:order_id>', methods=['PUT'])
@Auth.token_required
def update_order(current_user, order_id):
    """Updates the status of a given order"""
    data = request.get_json()
    new_status = data['status']
    new_time = datetime.datetime.now()
    order = order_inst.find_order_by_id(order_id)
    if order:
        response = order_inst.update_order(order_id, new_status, new_time)
        if response:
            return jsonify({'Message': 'Order updated'}), 200
    return jsonify({'Message': 'Order not found'}), 404


@order_v1.route('<int:order_id>', methods=['DELETE'])
@Auth.token_required
def cancel_order(current_user, order_id):
    """Owner cancels user order and deletes it from the storage"""
    order = order_inst.find_order_by_id(order_id)
    if order:
        if current_user['username'] == order['user_id']:
            order_inst.cancel_order(order_id)
            return jsonify({'Message': 'Order cancelled'}), 200
        return jsonify(
            {"Message": "Not authorized to cancel this order"}), 401  # to test

    return jsonify({'Message': 'Order not found'}), 404
