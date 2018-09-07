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
        """Home endpoint"""
        return '<h2 style="color: yellow;">Welcome to Fast-Food-Fast API<h2>\
        <h3>Endpoints (All order endpoints require auth):</h3>\
            <i>(To be tested on postman)<i><br><br>\
            POST: /api/v1/auth/register<br>POST: /api/v1/auth/login<br>\
            POST: /api/v1/orders<br>GET: /api/v1/orders/order_id<br>\
            GET: /api/v1/orders<br>PUT: /api/v1/orders/order_id<br>\
            DELETE: /api/v1/orders/order_id<br><br>\
            <h4>Sample user register data:</h4>\
            {<br>"first_name": "Kunta",<br>"last_name": "Kinte",<br>"username": "kunta.kinte",<br>\
            "email": "kuntatest@gmail.com",<br>"password": "@Password1"<br>\
            }<br><br><h4>Sample order data:</h4>{<br>"items": {"sausage": 2, "pizza": 3}<br>\
            }<br><h4>Available menu items:</h4>\
            {<br>"burger": 800,<br>"pizza": 1000,<br>"coffee": 300,<br>\
                "sausage": 100,<br>"rice": 500<br>\
            }'
    return app
