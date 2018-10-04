"""Menu Tests module"""
import json
import unittest
from tests.v2.test_setup import TestSetup


class TestMenu(TestSetup):
    """Include all the menu test methods"""
    def test_menu_access_with_invalid_token(self):
        """Raise unauthorized error invalid token."""
        response = self.client.post("/api/v2/menu",
                                    data=json.dumps(self.menu_item),
                                    content_type="application/json",
                                    headers={"x-access-token": "Wrong token"})
        self.assertEqual(response.status_code, 401)

    def test_menu_access_with_mising_token(self):
        """Raise unauthorized error missing token."""
        response = self.client.post("/api/v2/menu",
                                    data=json.dumps(self.menu_item),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_add_new_menu(self):
        """Tests creating a new menu."""
        response = self.client.post('/api/v2/menu',
                                    data=json.dumps(self.menu_item),
                                    content_type="application/json",
                                    headers={"x-access-token": self.admintoken})
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("added", response_msg["Message"])
        self.assertEqual(response.status_code, 201)

    def test_empty_name(self):
        """Error raised for blank menu name.
        A menu must have  a name."""
        response = self.client.post("/api/v2/menu",
                                    data=json.dumps(dict(name="",\
                                    price=200.00, image="empty.jpg", category="none")),
                                    content_type="application/json",
                                    headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("empty", response_msg["Message"])

    def test_duplicates_prevented(self):
        """
        Error raised for duplicate menu names.
        """
        self.client.post("/api/v2/menu",
                         data=json.dumps(self.menu_item),
                         content_type="application/json",
                         headers={"x-access-token": self.admintoken})
        response = self.client.post("/api/v2/menu",
                                    data=json.dumps(dict(name="fajita",
                                                         image="fajita.jpg",
                                                         price=800.00,
                                                         category="main")),
                                    content_type="application/json",
                                    headers={"x-access-token": self.admintoken})
        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("already exists", response_msg["Message"])

    def test_menu_list(self):
        """Test returns full menu"""
        resp = self.client.get('/api/v2/menu')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_menu_detail_200(self):
        """Test if you can get a single menu.
        Register a single menu first"""
        self.client.post("/api/v2/menu",
                         data=json.dumps(self.menu_item),
                         content_type="application/json",
                         headers={"x-access-token": self.admintoken})
        resp = self.client.get(
            '/api/v2/menu/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_invalid_menu_request(self):
        """
        Error raised for invalid menu request.
        """
        resp = self.client.get("/api/v2/menu/1000")
        self.assertEqual(resp.status_code, 404)
        response_msg = json.loads(resp.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_update_menu(self):
        """Tests a menu can be updated."""
        self.client.post("/api/v2/menu",
                         data=json.dumps(self.menu_item),
                         content_type="application/json",
                         headers={"x-access-token": self.admintoken})
        response = self.client.put(
            "/api/v2/menu/1",
            data=json.dumps(
                self.new_menu_item),
            content_type="application/json",
            headers={
                "x-access-token": self.admintoken})
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("updated", response_msg["Message"])

    def test_invalid_update(self):
        """Error raised for invalid update request."""
        response = self.client.put("/api/v2/menu/1000",
                                   data=json.dumps(self.new_menu_item),
                                   content_type="application/json",
                                   headers={"x-access-token": self.admintoken})

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_updating_unauthorized_menu(self):
        """Tests error raised when normal user try update menu."""
        response = self.client.put(
            "/api/v2/menu/2",
            data=json.dumps(
                self.new_menu_item),
            content_type="application/json",
            headers={
                "x-access-token": self.token})

        self.assertEqual(response.status_code, 403)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Not authorized", response_msg["Message"])


    def test_delete_menu(self):
        """Tests menu deletion."""
        self.client.post("/api/v2/menu",
                         data=json.dumps(self.menu_item),
                         content_type="application/json",
                         headers={"x-access-token": self.admintoken})
        response = self.client.delete(
            "/api/v2/menu/1",
            content_type="application/json",
            headers={
                "x-access-token": self.admintoken})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("deleted", response_msg["Message"])

    def test_deleting_unauthorized_menu(self):
        """Tests error raised when deleting if not admin."""
        response = self.client.delete(
            "/api/v2/menu/1",
            content_type="application/json",
            headers={
                "x-access-token": self.unkowntoken})

        self.assertEqual(response.status_code, 403)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Not authorized", response_msg["Message"])

    def test_invalid_delete(self):
        """Error raised for invalid delete request."""
        response = self.client.delete("/api/v2/menu/1000",
                                      content_type="application/json",
                                      headers={"x-access-token": self.admintoken})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_delete_with_invalid_token(self):
        """Test return invalid if token is invalid"""
        response = self.client.delete(
            "/api/v2/menu/1",
            content_type="application/json",
            headers={
                "x-access-token": "dd"})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Invalid", response_msg["Message"])


if __name__ == "__main__":
    unittest.main()
