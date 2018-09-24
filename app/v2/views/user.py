from flask import request, jsonify, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

#Local imports
from ...shared.authentication import Auth
from ...shared.validation import validate_user
from v2.models.user import User
from v2.database import Database

user_v2 = Blueprint('v2_user', __name__)
db = Database()
cur = db.cursor()

@user_v2.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if validate_user(data):
        return validate_user(data)
    user_inst = User(data['first_name'], data['last_name'], data['username'], data['email'], data['password'])
    try:
        success= user_inst.save_user()
        if not success:
            raise ValueError
        return jsonify({"Message": "User registered successfully"}), 201
    except ValueError:
        return jsonify({"Message": "User already exists"}), 400

@user_v2.route('/login', methods=['POST'])
def login():
    """Log in and generate token"""
    auth = request.get_json()
    if not auth or not auth['username'] or not auth['password']:
        return jsonify({"Message": "Username and password required!"}), 401

    try:
        query = "SELECT username, password FROM users WHERE username=%s;"
        cur.execute(query, (auth['username'],))
        row = cur.fetchone()
    except Exception as e:
        return str(e)
    if row:
        if check_password_hash(row['password'], auth['password']):
            u_token = jwt.encode({'username': row['username'],
                                'exp': datetime.datetime.utcnow() +
                                datetime.timedelta(minutes=30)},
                            os.getenv('SECRET'))
            u_token = u_token.decode('UTF-8')
            query = "INSERT INTO tokens(token) VALUES(%s)"
            cur.execute(query, (u_token,))
            db.connection.commit()
            # decode to string since python3 returns token in bytes
            return jsonify({"Message": "Login Success",
                        "token": u_token}), 200

        return jsonify({"Message": "login invalid!"}), 401

    return jsonify({"Message": "Username not found!"}), 401

    