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
        return 'Welcome to Fast-Food-Fast API'

    return app
