import os

from app import create_app
from app.v2.models.user import User

#Create a super to who can promote users to admin
super_user = User()
super_user.save_user()

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

if __name__ == '__main__':
    app.run(debug=True)
