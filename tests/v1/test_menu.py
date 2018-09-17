import json
import unittest
from tests.v1.test_setup import TestSetup


class TestMenu(TestSetup):
    def test_menu_access_with_invalid_token(self):
        """Raise unauthorized error invalid token."""
        response = self.client.post("/api/v1/menu",
                                    data=json.dumps(self.menu),
                                    content_type="application/json",
                                    headers={"x-access-token": "Wrong token"})
        self.assertEqual(response.status_code, 401)

    def test_menu_access_with_mising_token(self):
        """Raise unauthorized error missing token."""
        response = self.client.post("/api/v1/menu",
                                    data=json.dumps(self.menu),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_add_new_menu(self):
        """Tests creating a new menu."""
        response = self.client.post('/api/v1/menu',
                                    data=json.dumps(self.menu),
                                    content_type="application/json",
                                    headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("menu", response_msg["Message"])

    def test_empty_name(self):
        """Error raised for blank menu name.
        A menu must have  a name."""
        response = self.client.post("/api/v1/menu",
                                    data=json.dumps(dict(name="")),
                                    content_type="application/json",
                                    headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_duplicates_prevented(self):
        """
        Error raised for duplicate menu names.
        """
        self.client.post("/api/v1/menu",
                         data=json.dumps(self.menu),
                         content_type="application/json",
                         headers={"x-access-token": self.token})
        response = self.client.post("/api/v1/menu",
                                    data=json.dumps(dict(name="rice",
                                                         image="rice.jpg",
                                                         price=800,
                                                         category="main")),
                                    content_type="application/json",
                                    headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("already exists", response_msg["Message"])

    def test_menu_list(self):
        resp = self.client.get('/api/v1/menu')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_menu_detail_200(self):
        """Test if you can get a single menu.
        Register a single menu first"""
        resp = self.client.get(
            '/api/v1/menu/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_invalid_menu_request(self):
        """
        Error raised for invalid menu request.
        """
        resp = self.client.get("/api/v1/menu/1000")
        self.assertEqual(resp.status_code, 400)
        response_msg = json.loads(resp.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_update_menu(self):
        """Tests a menu can be updated."""
        response = self.client.put(
            "/api/v1/menu/1",
            data=json.dumps(
                self.new_menu),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("updated", response_msg["Message"])

    def test_invalid_update(self):
        """Error raised for invalid update request."""
        response = self.client.put("/api/v1/menu/1000",
                                   data=json.dumps(self.new_menu),
                                   content_type="application/json",
                                   headers={"x-access-token": self.token})

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_updating_unauthorized_menu(self):
        """Tests error raised when normal user try update menu."""
        response = self.client.put(
            "/api/v1/menus/1",
            data=json.dumps(
                self.new_menu),
            content_type="application/json",
            headers={
                "x-access-token": self.unkowntoken})

        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Unauthorized", response_msg["Message"])

    def test_duplicate_updates(self):
        """
        Tests for updating menu to a name that already exists.
         """
        self.client.post("/api/v1/menu",
                         data=json.dumps(dict(name="rice",
                                              image="rice.jpg",
                                              price=800,
                                              category="main")),
                         content_type="application/json",
                         headers={"x-access-token": self.token})
        response = self.client.put("/api/v1/menus/1",
                                   data=json.dumps(self.menu),
                                   content_type="application/json",
                                   headers={
                                       "x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("already exists", response_msg["Message"])

    def test_delete_menu(self):
        """Tests menu deletion."""
        response = self.client.delete(
            "/api/v1/menus/1",
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("deleted", response_msg["Message"])

    def test_deleting_unauthorized_menu(self):
        """Tests error raised when deleting if not admin."""
        response = self.client.delete(
            "/api/v1/menu/1",
            content_type="application/json",
            headers={
                "x-access-token": self.unkowntoken})

        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Unauthorized", response_msg["Message"])

    def test_invalid_delete(self):
        """Error raised for invalid delete request."""
        response = self.client.delete("/api/v1/menu/1000",
                                      content_type="application/json",
                                      headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_delete_with_invalid_token(self):
        """Test return invalid if token is invalid"""
        response = self.client.delete(
            "/api/v1/menu/1",
            content_type="application/json",
            headers={
                "x-access-token": "dd"})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Invalid", response_msg["Message"])


if __name__ == "__main__":
    unittest.main()
