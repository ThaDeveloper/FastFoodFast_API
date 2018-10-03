"""User View endpoints"""
import os
import datetime
import jwt
from flask import request, jsonify, Blueprint
from werkzeug.security import check_password_hash

# #Local imports
from app.v2.database import Database
from app.v2.models.user import User
from app.v2.models.order import Order
from .. utils.authentication import Auth
from ...shared.validation import validate_user
from ...shared.validation import ValidationError


USER_V2 = Blueprint('v2_user', __name__)
DB = Database()
CUR = DB.cursor()
ORDER = Order()
order_inst = Order()


@USER_V2.route('/register', methods=['POST'])
def register_user():
    """Adds user to the database, data must be serialized"""
    data = request.get_json()
    try:
        if validate_user(data):
            return validate_user(data)
        user_inst = User(
            data['first_name'],
            data['last_name'],
            data['username'],
            data['email'],
            data['password'])
    
    except KeyError as e:
        return jsonify({"Message": str(e) + " field is missing"}), 500
    try:
        query = "SELECT email from users where email=%s"
        CUR.execute(query, (data['email'],))
        row = CUR.fetchone()
        if row:
            return jsonify({"Message": "Email already registered"}), 409
        success = user_inst.save_user()
        if not success:
            raise ValueError
        return jsonify({"Message": "User registered successfully"}), 201
    except ValueError:
        return jsonify({"Message": "User already exists"}), 409


@USER_V2.route('/login', methods=['POST'])
def login():
    """Log in and generate token"""
    auth = request.get_json()
    if not auth or not auth['username'] or not auth['password']:
        return jsonify({"Message": "Username and password required!"}), 401

    try:
        query = "SELECT username, password FROM users WHERE username=%s;"
        CUR.execute(query, (auth['username'],))
        row = CUR.fetchone()
    except Exception as e:
        return str(e)
    if row:
        if check_password_hash(row['password'], auth['password']):
            u_token = jwt.encode({'username': row['username'],
                                  'exp': datetime.datetime.utcnow() +
                                         datetime.timedelta(minutes=30)},
                                 os.getenv('SECRET'))
            u_token = u_token.decode('UTF-8')
            query = "INSERT INTO tokens(user_id, token) VALUES(%s, %s)"
            CUR.execute(query, (auth['username'], u_token,))
            DB.connection.commit()
            # decode to string since python3 returns token in bytes
            return jsonify({"Message": "Login Success",
                            "token": u_token}), 200

        return jsonify({"Message": "login invalid!"}), 401

    return jsonify({"Message": "Username not found!"}), 401


@USER_V2.route('/logout', methods=['DELETE'])
@Auth.token_required
def logout(current_user):
    """Blacklists the tokens of the current logged in
    user. If logged out gives an error"""
    log_token = request.headers['x-access-token']
    query = "SELECT token FROM blacklist WHERE user_id=%s;"
    CUR.execute(query, (current_user['username'],))
    row = CUR.fetchone()
    def del_from_tokens(token):
        q = "DELETE FROM tokens WHERE token=%s;"
        CUR.execute(q, (token,))
        return DB.connection.commit()
    if row:
        if log_token == row['token']:
            return jsonify({"Message": "Already logged out"}), 400
        query = "UPDATE blacklist SET token=%s WHERE user_id=%s"
        CUR.execute(query, (log_token, current_user['username']))
        DB.connection.commit()
        #delete the token from tokens table
        del_from_tokens(log_token)
        return jsonify({"Message": "Successfully logged out"}), 200
    query = "INSERT INTO blacklist(user_id, token) VALUES(%s, %s);"
    CUR.execute(query, (current_user['username'], log_token,))
    DB.connection.commit()
    del_from_tokens(log_token)
    CUR.close
    return jsonify({"Message": "Successfully logged out"}), 200

@USER_V2.route('/users/<int:id>/promote', methods=['PUT'])
@Auth.token_required
def promote_user(current_user, id):
    """Change normal user to admin - Only preadded Superuser
    can access this route. Not available to public"""
    if current_user['username'] == 'superuser':
        user_inst = User()
        user = user_inst.get_user_by_id(id)
        if user:
            query = "UPDATE users SET admin=%s WHERE id=%s"
            CUR.execute(query, (True, id))
            DB.connection.commit()
            return jsonify({"Message": "User is now an admin!"}), 200
        return jsonify({"Message": "User not found!"}), 404

    return jsonify({"Message": "Sorry that route is not available to you!"}), 401

@USER_V2.route('/users/orders', methods=['POST'])
@Auth.token_required
def place_order(current_user):
    """Add order
    Needs to be logged in"""
    data = request.get_json()
    user = current_user['id']
    order_inst = Order()
    try:
        sanitized = order_inst.import_data(data)
        if sanitized == "Invalid":
            return jsonify({'Message': 'Order cannot be empty'}), 400
    except ValidationError as e:
        return jsonify({"Message": str(e)}), 400
    total = order_inst.total_cost(data['items'])
    if len(total[1]) > 0:
        return jsonify({"Message": "Some item(s) are out of stock:" + ','.join(total[1])+\
        ". Please edit your order to something else"}), 406 #Not acceptable
    try:
        order_inst = Order(
            user,
            str(data['items']),
            total[0])
    except KeyError as e:
        return jsonify({'Message': e.args[0] + ' field is required'}), 500
    success = order_inst.create_order()
    if not success:
        raise ValueError
    return jsonify({
        'Message': 'Order added',
        'Data':{
            'Items': data['items']
        }
        }), 201

@USER_V2.route('/users/orders', methods=['GET'])
@Auth.token_required
def view_orders(current_user):
    """Returns order history of logged in user"""
    query = "SELECT * FROM orders WHERE user_id=%s"
    CUR.execute(query, (current_user['id'],))
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
    return jsonify({"Message": "You have 0 orders"}), 200

@USER_V2.route('/users/orders/<int:order_id>', methods=['PUT'])
@Auth.token_required
def edit_order(current_user, order_id):
    """edit order by specified id"""
    data = request.get_json()
    new_time = datetime.datetime.now()
    try:
        for item in data['items']:
            if len(item) == 0:
                return jsonify({"Message": "Order items cannot be empty"}), 406
        new_total = order_inst.total_cost(data['items'])
    except KeyError as e:
        return jsonify({'Message': e.args[0] + ' field is required'}), 500
    if len(new_total[1]) > 0:
        return jsonify({"Message": "Some item(s) are out of stock:" + ','.join(new_total[1])+\
        ". Please edit your order to something else"}), 406 #Not acceptable
    order = order_inst.find_order_by_id(order_id)
    if order:
        if current_user['id'] == order['user_id']:
            response = ORDER.edit_order(
                order_id,
                str(data['items']),
                new_total[0],
                new_time)
            if response:
                return jsonify({"Message": "Order updated"}), 201
        return jsonify({"Message": "Not authorized to edit order"}), 403
    return jsonify({"Message": "Order not found"}), 404


@USER_V2.route('/users/orders/<int:order_id>', methods=['DELETE'])
@Auth.token_required
def cancel_order(current_user, order_id):
    """Owner cancels user order and deletes it from the storage"""
    order = order_inst.find_order_by_id(order_id)
    if order:
        if current_user['id'] == order['user_id']:
            order_inst.delete_order(order_id)
            return jsonify({'Message': 'Order cancelled'}), 200
        return jsonify(
            {"Message": "Not authorized to cancel this order"}), 403
    return jsonify({"Message": "Order not found"}), 404
