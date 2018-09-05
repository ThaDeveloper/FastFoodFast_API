import json
import unittest
from app.v1.app import create_app
from app.v1.models.order import Order
from app.v1.models.user import User


class TestSetup(unittest.TestCase):
    """Initialize the app with test data"""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.order = {"owner": "justin", "items": {"burger": 2, "coffee": 1}}
        self.empty_order = {"owner": "", "items": {}}
        order_inst = Order()
        user_inst = User()
        self.orders = order_inst.orders
        self.users = user_inst.users
        self.user = {"first_name": "Justin",
                     "last_name": "Ndwiga",
                     "username": "justin.ndwiga",
                     "email": "ndwigatest@gmail.com",
                     "password": "@Password1"}

        self.unknownuser = {"first_name": "Unknown",
                            "last_name": "User",
                            "username": "uknownuser",
                            "email": "uknown@gmail.com",
                            "password": "password"}

        # Register and login a testuser
        self.register = self.app.post('/api/v1/auth/register',
                                      data=json.dumps(self.user),
                                      headers={"content-type":
                                               "application/json"})
        self.login = self.app.post('/api/v1/auth/login',
                                   data=json.dumps(self.user),
                                   content_type='application/json')
        self.data = json.loads(self.login.get_data(as_text=True))
        self.token = self.data['token']

        # Register and login a testunkownuser
        self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(
                self.unknownuser),
            content_type="application/json")
        
        self.unkownlogin = self.app.post("/api/v1/auth/login",
                                         data=json.dumps(self.unknownuser),
                                         content_type="application/json")
        self.data = json.loads(self.unkownlogin.get_data(as_text=True))
        self.unkowntoken = self.data['token']


    def tearDown(self):
        self.orders.clear()
        self.users.clear()
