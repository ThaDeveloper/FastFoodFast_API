import json
import unittest
from app import create_app
from app.v1.models.order import Order
from app.v1.models.menu import Menu
from app.v1.models.user import User


class TestSetup(unittest.TestCase):
    """Initialize the app with test data
    All other test classes inherits from TestSetup"""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
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
        self.order = {"items": {"burger": 2, "pizza": 1}}
        self.new_order = {"items": {"burger": 1, "pizza": 3}}
        self.empty_order = {"items": {}}
        self.menu_item = {
            "name": "rice",
            "image": "rice.jpg",
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
        order_inst = Order()
        user_inst = User()
        menu_inst = Menu()
        self.orders = order_inst.orders
        self.menu = menu_inst.menu
        self.users = user_inst.users

        # Register and login a testuser
        self.register = self.client.post('/api/v1/auth/register',
                                         data=json.dumps(self.user),
                                         headers={"content-type":
                                                  "application/json"})
        self.login = self.client.post('/api/v1/auth/login',
                                      data=json.dumps(self.user),
                                      content_type='application/json')
        self.data = json.loads(self.login.get_data(as_text=True))
        self.token = self.data['token']

        #login test admin
        self.adminlogin = self.client.post('/api/v1/auth/login',
                                           data=json.dumps(dict(username=self.users['admin']['username'], password='password')),
                                           content_type='application/json')

        self.data = json.loads(self.adminlogin.get_data(as_text=True))
        self.admintoken = self.data['token']

        # Register and login a testunkownuser
        self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(
                self.unknownuser),
            content_type="application/json")

        self.unkownlogin = self.client.post("/api/v1/auth/login",
                                            data=json.dumps(self.unknownuser),
                                            content_type="application/json")
        self.data = json.loads(self.unkownlogin.get_data(as_text=True))
        self.unkowntoken = self.data['token']

    def tearDown(self):
        self.orders.clear()
        self.menu.clear()
        self.users.clear()
