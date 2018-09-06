import json
import unittest
from tests.v1.test_setup import TestSetup


class TestOrder(TestSetup):
    """All test cases for Order class"""

    def test_add_new_order(self):
        """Tests creating a new order."""
        response = self.app.post('/api/v1/orders',
                                 data=json.dumps(self.order),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Order", response_msg["Message"])

    def test_empty_items(self):
        """Error raised for empty order placed."""
        response = self.app.post("/api/v1/orders",
                                 data=json.dumps(dict(items="")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_order_list(self):
        """Test full list orders can be returned"""
        resp = self.app.get('/api/v1/orders')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_order_detail_200(self):
        """Test if you can get a single order.
        Make a single order first"""
        self.app.post('/api/v1/orders', data=json.dumps(self.order),
                      content_type="application/json")
        resp = self.app.get('/api/v1/orders/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_invalid_order_request(self):
        """
        Error raised for invalid order request.
        """
        resp = self.app.get("/api/v1/orders/15")
        self.assertEqual(resp.status_code, 404)
        response_msg = json.loads(resp.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_update_order(self):
        """Tests a order can be updated."""
        response = self.app.put("/api/v1/orders/1",
                                data=json.dumps(dict(status="accepted")),
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("accepted", response_msg["Message"])

    def test_invalid_update(self):
        """Error raised for invalid update request."""
        response = self.app.put("/api/v1/orders/15",
                                data=json.dumps(dict(status="accepted")),
                                content_type="application/json")

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_decline_order(self):
        """Tests order decline."""
        self.app.post(
            '/api/v1/orders',
            data=json.dumps(
                dict(
                    items="sausage", price=100, servings=2)),
            content_type="application/json")
        response = self.app.delete("/api/v1/orders/2",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("declined", response_msg["Message"])


if __name__ == "__main__":
    unittest.main()
