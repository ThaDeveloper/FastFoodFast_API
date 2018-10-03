"""Authentication class"""
import os
from functools import wraps
from flask import jsonify, request
import jwt


# Local imports
from .. database import Database
DB = Database()


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
                query = "SELECT * from users WHERE username=%s"
                cur = DB.cursor()
                cur.execute(query, (data['username'],))
                row = cur.fetchone()
                if row:
                    current_user = row
                else:
                    return jsonify(
                        {"Message": "Token expired:Login again"}), 401
            except BaseException as e:
                return jsonify({'Message': 'Invalid request:' + str(e)}), 401

            return f(current_user, *args, **kwargs)

        return decorated
