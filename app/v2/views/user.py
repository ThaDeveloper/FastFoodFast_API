import os
import datetime
import jwt
from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

# #Local imports
from .. utils.authentication import Auth
from ...shared.validation import validate_user
from app.v2.models.user import User
from app.v2.database import Database

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
            query = "INSERT INTO tokens(user_id, token) VALUES(%s, %s)"
            cur.execute(query, (auth['username'],u_token,))
            db.connection.commit()
            # decode to string since python3 returns token in bytes
            return jsonify({"Message": "Login Success",
                        "token": u_token}), 200

        return jsonify({"Message": "login invalid!"}), 401

    return jsonify({"Message": "Username not found!"}), 401

@user_v2.route('/logout', methods=['DELETE'])
@Auth.token_required
def logout(current_user):
    """Blacklists the tokens of the current logged in
    user. If logged out gives an error"""
    log_token = request.headers['x-access-token']
    query = "SELECT token FROM blacklist WHERE user_id=%s;"
    cur.execute(query, (current_user['username'],))
    row = cur.fetchone()
    if row:
        if log_token == row['token']:
            return jsonify({"Message": "Already logged out"}), 400
        query = "UPDATE blacklist SET token=%s WHERE user_id=%s"
        cur.execute(query, (log_token, current_user['username']))
        db.connection.commit()
        return jsonify({"Message": "Successfully logged out"}), 200
    query = "INSERT INTO blacklist(user_id, token) VALUES(%s, %s);"
    cur.execute(query, (current_user['username'], log_token,))
    db.connection.commit()
    cur.close
    return jsonify({"Message": "Successfully logged out"}), 200
        
    
    