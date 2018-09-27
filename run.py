import os

from app import create_app

ENV_NAME = os.getenv('FLASK_ENV')
APP = create_app(ENV_NAME)

if __name__ == '__main__':
    APP.run(debug=True)
