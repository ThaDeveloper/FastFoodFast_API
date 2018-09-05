import json
import unittest
from app.v1.app import create_app
from app.v1.models.order import Order


class TestSetup(unittest.TestCase):
    """Initialize the app with test data"""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.order = {"owner": "justin","items": "pizza", "servings": 2}
        self.empty_order = {"owner": "","items": "", "servings": ""}
        order_inst = Order()
        self.orders = order_inst.orders
    
    def tearDown(self):
        self.orders.clear()