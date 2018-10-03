"""Apps entry point"""
import os

from app import create_app
from app.v2.models.user import User

#Create a super to who can promote users to admin
super_user = User()
super_user.save_user()

ENV_NAME = os.getenv('FLASK_ENV')
APP = create_app(ENV_NAME)

if __name__ == '__main__':
    APP.run(debug=True)
