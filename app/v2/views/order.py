"""Order endpoints"""
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
        return jsonify({"Message": "No orders found"}), 200
    return jsonify({"Message": "Not authorized to view orders"}), 401


@ORDER_V2.route('/<int:order_id>', methods=['GET'])
@Auth.token_required
def get_single_order(current_user, order_id):
    """Return specific order by id"""
    order = ORDER.find_order_by_id(order_id)
    if order:
        if current_user['admin']:
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
        return jsonify({"Message": "Not authorized to view this order"}), 401
    return jsonify({"Message": "Order not found"}), 404

