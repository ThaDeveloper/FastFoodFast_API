"""Flask app initialization"""
from flask import Flask
from flask_cors import CORS

from config import APP_CONFIG

# Import blueprints
from . v1.views.order import order_v1 as order_blueprint
from . v1.views.user import user_v1 as user_blueprint
from . v1.views.menu import menu_v1 as menu_blueprint
from . v2.views.user import USER_V2 as v2_user_blueprint
from . v2.views.menu import MENU_V2 as v2_menu_blueprint
from . v2.utils.error_handling import *


def create_app(env_name):
    """
    Create app returns a new flask app object
    """

    # app initiliazation
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(APP_CONFIG[env_name])

    app.register_blueprint(order_blueprint, url_prefix='/api/v1/orders')
    app.register_blueprint(user_blueprint, url_prefix='/api/v1/auth')
    app.register_blueprint(menu_blueprint, url_prefix='/api/v1/menu')
    app.register_blueprint(v2_user_blueprint, url_prefix='/api/v2/auth')
    app.register_blueprint(v2_menu_blueprint, url_prefix='/api/v2/menu')
    app.register_error_handler(404, page_404)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(405, method_not_found)


    @app.route('/', methods=['GET'])
    def index():
        """Home endpoint"""
        return '<h2 style="color: yellow;">Welcome to Fast-Food-Fast API<h2>\
        <h3>Endpoints (All order endpoints require auth):</h3>\
            <i>(To be tested on postman)<i><br><br>\
            <h5>USER:</h5>\
            POST: /api/v1/auth/register<br>POST: /api/v1/auth/login<br>\
            <h5>ORDER:</h5>\
            POST: /api/v1/orders<br>GET: /api/v1/orders/order_id<br>\
            GET: /api/v1/orders<br>PUT: /api/v1/orders/order_id<br>\
            PUT: /api/v1/orders/order_id/edit<br>DELETE: /api/v1/orders/order_id<br><br>\
            GET: /api/v1/orders/customer<br>\
            <h5>MENU<h5>\
            POST: /api/v1/menu<br>GET: /api/v1/menu<br>\
            GET: /api/v1/menu/menu_id<br>PUT: /api/v1/menu/menu_id<br>\
            DELETE: /api/v1/menu/menu_id<br>\
            <h4>Sample user register data:</h4>\
            {<br>"first_name": "Kunta",<br>"last_name": "Kinte",<br>"username": "kunta.kinte",<br>\
            "email": "kuntatest@gmail.com",<br>"password": "#123pass"<br>\
            }<br><br><h4>Sample order data:</h4>{<br>"items": {"burger": 2, "pizza": 3}<br>\
            }<br><h4>Available pre-added menu items:</h4>\
            {<br>"burger": 800,<br>"pizza": 1000<br>\
            }'
    return app
