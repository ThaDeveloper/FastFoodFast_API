"""User View"""
import os
import datetime
from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from ...v1.authentication import user_inst
from ...shared.validation import validate_user

user_v1 = Blueprint('user', __name__)


@user_v1.route('/register', methods=['POST'])
def register_user():
    """Receives user data as json object"""
    data = request.get_json()
    password_hash = generate_password_hash(data['password'], method='sha256')
    if data['username'] in user_inst.users:
        return jsonify({'Message': "User already exists"}), 400
    email_list = [user['email'] for user in list(user_inst.users.values())]
    if data['email'] in email_list:
        return jsonify({'Message': "Email already registered"}), 400
    if validate_user(data):
        return validate_user(data)
    data = user_inst.create_user(
        data['first_name'],
        data['last_name'],
        data['username'],
        data['email'],
        password_hash)
    return jsonify({"Message": "User registered successfully"}), 201


@user_v1.route('/login', methods=['POST'])
def login():
    """Log in and generate token"""
    auth = request.get_json()
    if not auth or not auth['username'] or not auth['password']:
        return jsonify({"Message": "Username and password required!"}), 401

    if auth['username'] not in user_inst.users.keys():
        return jsonify({"Message": "Username not found!"}), 401

    user = user_inst.users[auth['username']]
    if check_password_hash(user['password'], auth['password']):
        token = jwt.encode({'username': user['username'],
                            'exp': datetime.datetime.utcnow() +
                                   datetime.timedelta(minutes=30)},
                           os.getenv('SECRET'))
        user_inst.u_token[user['username']] = token
        # decode to string since python3 returns token in bytes
        return jsonify({"Message": "Login Success",
                        "token": token.decode('UTF-8')}), 200

    return jsonify({"Message": "login invalid!"}), 401
