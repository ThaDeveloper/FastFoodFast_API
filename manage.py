import os
from flask_script import Manager

#Local import
from app import create_app
from app.v2.database import Database

db = Database()

#flask app instance
env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

#manager requires a flask instance
manager = Manager(app)

#running the 'create_db' command will create all the tables
@manager.command
def create_db():
    """Initialize database and create all tables"""
    db.create_tables()

@manager.command
def drop_db():
    """drop all database tables"""
    db.drop_tables()

if __name__ == '__main__':
    manager.run()