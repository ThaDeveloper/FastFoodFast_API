from flask import Flask

from config import app_config

#Import order_api blueprint
from .views.order import order_v1 as order_blueprint

def create_app(env_name):
  """
  Create app returns a new flask app object
  """
  
  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  app.register_blueprint(order_blueprint, url_prefix='/api/v1/orders')
  @app.route('/', methods=['GET'])
  def index():
    """
    Home endpoint
    """
    return 'Welcome to Fast-Food-Fast API'

  return app