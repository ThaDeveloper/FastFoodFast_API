import json
import unittest
from tests.v1.test_setup import TestSetup


class TestOrder(TestSetup):
    """All test cases for Order class"""

    def test_add_new_order(self):
        """Tests creating a new order."""
        response = self.client.post('/api/v1/orders',
                                 data=json.dumps(self.order),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Order", response_msg["Message"])

    def test_empty_items(self):
        """Error raised for empty order placed."""
        response = self.client.post("/api/v1/orders",
                                 data=json.dumps(dict(owner="user", items="", servings=2)),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("empty", response_msg["Message"])

    def test_order_list(self):
        """Test full list orders can be returned"""
        resp = self.client.get('/api/v1/orders')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_order_detail_200(self):
        """Test if you can get a single order.
        Make a single order first"""
        resp = self.client.get('/api/v1/orders/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_invalid_order_request(self):
        """
        Error raised for invalid order request.
        """
        resp = self.client.get("/api/v1/orders/100")
        self.assertEqual(resp.status_code, 404)
        response_msg = json.loads(resp.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_update_order(self):
        """Tests a order can be updated."""
        response = self.client.put("/api/v1/orders/1",
                                data=json.dumps(dict(status="accepted")),
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("updated", response_msg["Message"])

    def test_invalid_update(self):
        """Error raised for invalid update request."""
        response = self.client.put("/api/v1/orders/15",
                                data=json.dumps(dict(status="accepted")),
                                content_type="application/json")

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_cancel_order(self):
        """Tests cancel order."""
        self.client.post(
            '/api/v1/orders',
            data=json.dumps(
                dict(
                    owner="user", items="sausage", servings=2)),
            content_type="application/json")
        response = self.client.delete("/api/v1/orders/2",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("cancelled", response_msg["Message"])


if __name__ == "__main__":
    unittest.main()
