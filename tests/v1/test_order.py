import json
import unittest
from tests.v1.test_setup import TestSetup


class TestOrder(TestSetup):
    """All test cases for Order class"""
    
    def test_add_new_order(self):
        """Tests creating a new order."""
        response = self.client.post(
            '/api/v1/orders',
            data=json.dumps(
                self.order),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Order", response_msg["Message"])

    def test_add_order_no_login(self):
        """Tests returns error when ordering without login."""
        response = self.client.post('/api/v1/orders',
                                    data=json.dumps(self.order),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("need to", response_msg["Message"])


    def test_add_order_with_invalid_token(self):
        """Tests returns error when ordering with invalid token."""
        response = self.client.post(
            '/api/v1/orders',
            data=json.dumps(
                self.order),
            content_type="application/json",
            headers={
                "x-access-token": "123-invalid[333]"})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Invalid", response_msg["Message"])

    def test_empty_items(self):
        """Error raised for empty order placed."""
        response = self.client.post(
            "/api/v1/orders",
            data=json.dumps(
                self.empty_order),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("empty", response_msg["Message"])

    def test_empty_field(self):
        """Error raised when ordder field is empty."""
        response = self.client.post(
            "/api/v1/orders",
            data=json.dumps(
                dict(
                    {})),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_order_list(self):
        """Test full list orders can be returned"""
        resp = self.client.get(
            '/api/v1/orders',
            headers={
                "x-access-token": self.token})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_order_history(self):
        """Test user order history is returned"""
        resp = self.client.get(
            '/api/v1/orders/customer',
            headers={
                "x-access-token": self.token})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_no_order_history(self):
        """Test returns 0 orders message to user"""
        self.client.delete(
            "/api/v1/orders/1",
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        resp = self.client.get(
            '/api/v1/orders/customer',
            headers={
                "x-access-token": self.token})
        response_msg = json.loads(resp.data.decode("UTF-8"))
        self.assertIn("0 orders", response_msg["Message"])

    def test_order_detail_200(self):
        """Test if you can get a single order.
        Make a single order first"""
        self.client.post('/api/v1/orders', data=json.dumps(self.order),
                         content_type="application/json",
                         headers={"x-access-token": self.token})
        resp = self.client.get(
            "/api/v1/orders/1",
            headers={
                "x-access-token": self.token})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_unauthorized_get_order(self):
        self.tearDown()
        """Test returns error for accessing someone elses business"""
        resp = self.client.get("/api/v1/orders/1",
                               headers={"x-access-token": self.unkowntoken})
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.content_type, 'application/json')

    def test_invalid_order_request(self):
        """
        Error raised for invalid order request.
        """
        resp = self.client.get(
            "/api/v1/orders/100",
            headers={
                "x-access-token": self.token})
        self.assertEqual(resp.status_code, 404)
        response_msg = json.loads(resp.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])
    
    def test_edit_order(self):
        """Tests a order can be editted."""
        response = self.client.put(
            "/api/v1/orders/1/edit",
            data=json.dumps(self.new_order),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("updated", response_msg["Message"])
    
    def test_invalid_edit(self):
        """Error raised for invalid edit request."""
        response = self.client.put(
            "/api/v1/orders/15/edit",
            data=json.dumps(self.new_order),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_editting_unauthorized_order(self):
        """Tests error raised when editting non-authorized order."""
        response = self.client.put("/api/v1/orders/1/edit",
                                   data=json.dumps(self.new_order),
                                   content_type="application/json",
                                   headers={
                                        "x-access-token": self.unkowntoken})

        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Not authorized", response_msg["Message"])

    def test_update_order(self):
        """Tests a order can be updated."""
        response = self.client.put(
            "/api/v1/orders/1",
            data=json.dumps(
                dict(
                    status="accepted")),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Order", response_msg["Message"])

    def test_invalid_update(self):
        """Error raised for invalid update request."""
        response = self.client.put(
            "/api/v1/orders/15",
            data=json.dumps(
                dict(
                    status="accepted")),
            content_type="application/json",
            headers={
                "x-access-token": self.token})

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_updating_unauthorized_order(self):
        """Tests error raised when updating order without login."""
        response = self.client.put("/api/v1/orders/1",
                                   data=json.dumps(dict(status="completed")),
                                   content_type="application/json")

        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("need to log in", response_msg["Message"])
    
    def test_cancel_invalid_order(self):
        """Tests cancel invalid order."""
        response = self.client.delete(
            "/api/v1/orders/200",
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_canelling_unauthorized_order(self):
        """Tests error raised when cancelling someone else's order."""
        response = self.client.delete(
            "/api/v1/orders/1",
            headers={
                "x-access-token": self.unkowntoken})

        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Not authorized", response_msg["Message"])

    def test_cancel_order(self):
        """Tests cancel order."""
        self.client.post(
            '/api/v1/orders',
            data=json.dumps(
                dict(
                    items={
                        "burger": 2})),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        response = self.client.delete(
            "/api/v1/orders/2",
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("cancelled", response_msg["Message"])

    
    def test_no_orders_found(self):
        """Test no orders in memory"""
        print(self.orders)
        resp = self.client.get(
            '/api/v1/orders',
            headers={
                "x-access-token": self.token})
        self.assertEqual(resp.status_code, 200)



if __name__ == "__main__":
    unittest.main()
