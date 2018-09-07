from flask import Flask
import os 
import sys
import inspect

from config import app_config

# Import order_api blueprint
from . v1.views.order import order_v1 as order_blueprint
from . v1.views.user import user_v1 as user_blueprint

def create_app(env_name):
    """
    Create app returns a new flask app object
    """

    # app initiliazation
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[env_name])

    app.register_blueprint(order_blueprint, url_prefix='/api/v1/orders')
    app.register_blueprint(user_blueprint, url_prefix='/api/v1/auth')

    @app.route('/', methods=['GET'])
    def index():
        """
        Home endpoint
        """
        return 'Welcome to Fast-Food-Fast API \n\
        Endpoints (All order endpoints require auth):\n\
            POST: /api/v1/auth/register\n\
            POST: /api/v1/auth/login\n\
            POST: /api/v1/orders\n\
            GET: /api/v1/orders/order_id\n\
            GET: /api/v1/orders\n\
            PUT: POST: /api/v1/orders/order_id\n\
            DELETE: POST: /api/v1/orders/order_id\n\n\
            Sample user register data:\n\
            {\n\
            "first_name": "Kunta",\n\
            "last_name": "Kinte",\n\
            "username": "kunta.kinte",\n\
            "email": "kuntatest@gmail.com",\n\
            "password": "@Password1"\n\
            }\n\
            Sample order data:\n\
            {\n\
	            "items": {"sausage": 2, "pizza": 3}\n\
            }\n\
            Available menu items:\n\
            {\n\
                "burger": 800,\n\
                "pizza": 1000,\n\
                "coffee": 300,\n\
                "sausage": 100,\n\
                "rice": 500\n\
            }'

    return app
