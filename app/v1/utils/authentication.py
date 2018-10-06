"""Authentication module"""
import os
from functools import wraps
from flask import jsonify, request
import jwt

from ..models.user import User

user_inst = User()


class Auth:
    """Creates a decorator for all the endpoints that needs authentication"""
    @staticmethod
    def token_required(f):
        """All endoints that need log in will be wrapped by this decorator"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                return jsonify({'Message': 'You need to log in'}), 401

            try:
                data = jwt.decode(token, os.getenv('SECRET'))
                if data['username'] in user_inst.u_token:
                    current_user = user_inst.users[data['username']]
                else:
                    return jsonify(
                        {"Message": "Token expired:Login again"}), 401
            except BaseException:
                return jsonify({'Message': 'Invalid request!'}), 401

            return f(current_user, *args, **kwargs)

        return decorated
