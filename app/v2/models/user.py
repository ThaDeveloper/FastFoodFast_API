"""User class module"""
from datetime import datetime
from werkzeug.security import generate_password_hash


#Local import
from .. database import Database

DB = Database()

class User:
    """Methods of the User model"""
    def __init__(self, first_name, last_name, username, email, password, admin=False):
        """initialize user model"""
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.admin = admin
        self.created_at = datetime.now()
        self.cur = DB.cursor()

    def check_user_exists(self, username):
        """Check if user exists"""
        query = "SELECT username FROM users WHERE username = %s;"
        self.cur.execute(query, (username,))
        return self.cur.fetchone() is not None

    def save_user(self):
        """Adds user to the database"""
        if self.check_user_exists(self.username):
            return False
        query = "INSERT INTO users (first_name, last_name, username, email, password,\
        admin, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        self.cur.execute(query, (self.first_name, self.last_name, self.username,\
        self.email, self.password, self.admin, self.created_at))
        DB.commit()
        self.cur.close()
        return True
 