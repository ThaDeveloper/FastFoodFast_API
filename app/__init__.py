"""Flask app initialization"""
from flask import Flask, render_template
from flask_cors import CORS
from config import APP_CONFIG
from . shared.error_handling import *

# Import blueprints
from . v1.views.order import order_v1 as order_blueprint
from . v1.views.user import user_v1 as user_blueprint
from . v1.views.menu import menu_v1 as menu_blueprint
from . v2.views.user import USER_V2 as v2_user_blueprint
from . v2.views.menu import MENU_V2 as v2_menu_blueprint
from . v2.views.order import ORDER_V2 as v2_order_blueprint
from config import app_config

def create_app(env_name):
    """
    Create app returns a new flask app object
    """

    # app initiliazation
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(APP_CONFIG[env_name])
    app.url_map.strict_slashes = False
    app.register_blueprint(order_blueprint, url_prefix='/api/v1/orders')
    app.register_blueprint(user_blueprint, url_prefix='/api/v1/auth')
    app.register_blueprint(menu_blueprint, url_prefix='/api/v1/menu')
    app.register_blueprint(v2_user_blueprint, url_prefix='/api/v2/auth')
    app.register_blueprint(v2_menu_blueprint, url_prefix='/api/v2/menu')
    app.register_blueprint(v2_order_blueprint, url_prefix='/api/v2/orders')
    app.register_error_handler(404, page_404)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(405, method_not_found)
    app.register_error_handler(504, timeout_504)

    @app.route('/', methods=['GET'])
    @app.route('/favicon.png', methods=['GET'])
    def index():
        """Home endpoint - render API documentation"""
        return render_template('version2.html')
    return app
