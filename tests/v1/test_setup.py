import json
import unittest
from app import app


class TestSetup(unittest.TestCase):
    """Initialize the app with test data"""

    def setUp(self):
        self.app = app.test_client()
        self.order = {"items":"pizza","price": 1000, "servings": 2}
        self.empty_order = {"items": "","price": "", "servings": ""}
