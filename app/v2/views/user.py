"""User View endpoints"""
import os
import datetime
import jwt
from flask import request, jsonify, Blueprint
from werkzeug.security import check_password_hash

# #Local imports
from app.v2.database import Database
from app.v2.models.user import User
from .. utils.authentication import Auth
from ...shared.validation import validate_user


USER_V2 = Blueprint('v2_user', __name__)
DB = Database()
CUR = DB.cursor()


@USER_V2.route('/register', methods=['POST'])
def register_user():
    """Adds user to the database, data must be serialized"""
    data = request.get_json()
    if validate_user(data):
        return validate_user(data)
    user_inst = User(
        data['first_name'],
        data['last_name'],
        data['username'],
        data['email'],
        data['password'])
    try:
        success = user_inst.save_user()
        if not success:
            raise ValueError
        return jsonify({"Message": "User registered successfully"}), 201
    except ValueError:
        return jsonify({"Message": "User already exists"}), 400


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
    return jsonify({"Message": "Successfully logged out"}), 200
