import os
from functools import wraps
from flask import jsonify, request
import jwt


# Local imports
from . database import Database
db = Database()


class Auth(object):
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
                print(data)
                query = "SELECT id,first_name, last_name, username, email, passowrd from users WHERE username=%s;"
                cur = db.cursor()
                cur.execute(query, (data['username'],))
                row = cur.fetchone()
                print(row)
                if row:
                    current_user = row
                else:
                    return jsonify(
                        {"Message": "Token expired:Login again"}), 401
            except BaseException:
                return jsonify({'Message': 'Invalid request!'}), 401

            return f(current_user, *args, **kwargs)

        return decorated
