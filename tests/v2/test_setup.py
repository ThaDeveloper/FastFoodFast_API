import os
import json
import unittest
from app import create_app
from app.v2.database import Database


class TestSetup(unittest.TestCase):
    """Initialize the app with test data
    All other test classes inherits from TestSetup"""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.db = Database()
        self.user = {"first_name": "Justin",
                     "last_name": "Ndwiga",
                     "username": "justin.ndwiga",
                     "email": "ndwigatest@gmail.com",
                     "password": "@Password1"}

        self.unknownuser = {"first_name": "Unknown",
                            "last_name": "User",
                            "username": "uknownuser",
                            "email": "uknown@gmail.com",
                            "password": "@Password2"}
        self.admin = {"first_name": "Super",
                            "last_name": "User",
                            "username": "admin",
                            "email": "admin@fast.com",
                            "password": "@Password1"}
        self.order = {"items": {"pizza": 2}}
        self.new_order = {"items": {"pizza": 10}}
        self.empty_order = {"items": {}}
        self.menu_item = {
            "name": "fajita",
            "image": "fajita.jpg",
            "price": 800,
            "category": "main"}
        self.new_menu_item = {
            "name": "beef steak",
            "image": "beef.jpg",
            "price": 1000,
            "category": "main"}
        self.empty_menu_item = {
            "name": "",
            "image": "",
            "price": "",
            "category": ""}

        # Register and login a testuser
        self.register = self.client.post('/api/v2/auth/register',
                                         data=json.dumps(self.user),
                                         headers={"content-type":
                                                  "application/json"})
        self.login = self.client.post('/api/v2/auth/login',
                                      data=json.dumps(self.user),
                                      content_type='application/json')
        self.data = json.loads(self.login.get_data(as_text=True))
        self.token = self.data['token']

        #Resgister and login test admin
        self.register = self.client.post('/api/v2/auth/register',
                                         data=json.dumps(self.admin),
                                         headers={"content-type":
                                                  "application/json"})
        #make the user admin and login
        q = "UPDATE users SET admin='true' WHERE username=%s;"
        self.db.cursor().execute(q, (self.admin['username'],))
        self.db.connection.commit()
        self.adminlogin = self.client.post('/api/v2/auth/login',
                                           data=json.dumps(self.admin),
                                           content_type='application/json')

        self.data = json.loads(self.adminlogin.get_data(as_text=True))
        self.admintoken = self.data['token']

        # Register and login a testunkownuser
        self.client.post(
            "/api/v2/auth/register",
            data=json.dumps(
                self.unknownuser),
            content_type="application/json")

        self.unkownlogin = self.client.post("/api/v2/auth/login",
                                            data=json.dumps(self.unknownuser),
                                            content_type="application/json")
        self.data = json.loads(self.unkownlogin.get_data(as_text=True))
        self.unkowntoken = self.data['token']

        #add one menu item to db
        q = "INSERT INTO menu(name, price, category, image) VALUES(%s,%s,%s,%s);"
        self.db.cursor().execute(q, ('pizza',900.00, 'snacks', 'image'))
        self.db.connection.commit()

    def tearDown(self):
        self.db.drop_tables()
        
if __name__ == "__main__":
    unittest.main()
