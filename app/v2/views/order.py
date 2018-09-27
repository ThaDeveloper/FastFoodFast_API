"""Order endpoints"""
from datetime import datetime
import psycopg2
from flask import request, jsonify, Blueprint

# #Local imports
from app.v2.database import Database
from app.v2.models.order import Order
from .. utils.authentication import Auth
from ...shared.validation import ValidationError


ORDER_V2 = Blueprint('v2_order', __name__)
DB = Database()
CUR = DB.cursor()
ORDER = Order()
order_inst = Order()


@ORDER_V2.route('', methods=['POST'])
@Auth.token_required
def place_order(current_user):
    """Add order
    Needs to be logged in"""
    data = request.get_json()
    user = current_user['id']
    order_inst = Order()
    total = order_inst.total_cost(data['items'])
    if not total:
        return jsonify({"Message": "Menu item not found"}), 400
    order_inst = Order(
        user,
        data['items'],
        total)
    try:
        sanitized = order_inst.import_data(data)
        if sanitized == "Invalid":
            return jsonify({'Message': 'Order cannot be empty'}), 400
    except ValidationError as e:
        return jsonify({"Message": str(e)}), 400
    success = order_inst.create_order()
    if not success:
        raise ValueError
    return jsonify({'Message': 'Order added'}), 201


@ORDER_V2.route('', methods=['GET'])
@Auth.token_required
def view_orders(current_user):
    if current_user['admin']:
        query = "SELECT * FROM orders"
        CUR.execute(query)
        orders = CUR.fetchall()
        if orders:
            return jsonify({
                "Orders": [
                    {
                        'id': order['order_id'],
                        'user_id': order['user_id'],
                        'items': order['items'],
                        'total': '%.*f' % (2, order['total']),
                        'status': order['status'],
                        'created_at': order['created_at'],
                        'updated_at':order['updated_at']
                    } for order in orders
                ]

            }), 200
        return jsonify({"Message": "No Menu found"}), 200
    return jsonify({"Message": "Not authorized to view orders"}), 401


@ORDER_V2.route('/<int:order_id>', methods=['GET'])
@Auth.token_required
def get_single_order(current_user, order_id):
    if current_user['admin']:
        """Return specific order by id"""
        order = ORDER.find_order_by_id(order_id)
        if order:
            return jsonify({
                'Order': [
                    {
                        'id': order['order_id'],
                        'user_id': order['user_id'],
                        'items': order['items'],
                        'total': '%.*f' % (2, order['total']),
                        'status': order['status'],
                        'created_at': order['created_at'],
                        'updated_at':order['updated_at']
                    }
                ]
            }), 200
        return jsonify({"Message": "Order not found"}), 404
    return jsonify({"Message": "Not authorized to view orders"}), 401


@ORDER_V2.route('/<int:order_id>', methods=['PUT'])
@Auth.token_required
def edit_menu_item(current_user, order_id):
    """edit order by specified id"""
    data = request.get_json()
    new_time = datetime.now()
    new_total = order_inst.total_cost(data['items'])
    if current_user['admin']:
        response = ORDER.edit_order(
            order_id,
            data['items'],
            new_total,
            new_time)
        if response:
            return jsonify({"Message": "Order updated"}), 201
        return jsonify({"Message": "Order not found"}), 404

    return jsonify({"Message": "Not authorized to edit order"}), 401
