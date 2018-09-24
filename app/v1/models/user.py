import uuid


class User(object):
    """Store user data in dictionaries"""

    def __init__(self):
        self.users = {}
        self.u_token = {}

    def create_user(
            self,
            first_name,
            last_name,
            username,
            email,
            password,
            admin=False):
        """Creates a new user an append to the list of users"""
        data = {'id': str(uuid.uuid4()),
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'password': password,
                'admin': admin}
        self.users[username] = data
        return self.users
