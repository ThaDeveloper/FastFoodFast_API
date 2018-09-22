import unittest
import json
from tests.v1.test_setup import TestSetup


class TestUser(TestSetup):
    """Test user authorization."""

    def test_missing_username(self):
        """tests returns error if username is missing."""
        response = self.client.post(
            "api/v1/auth/register", data=json.dumps(
                dict(
                    first_name="blank",
                    last_name="username",
                    username="",
                    email="blank@gmail.com",
                    password="@Password5")),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("3-15 alpha-numeric", response_msg["Message"])

    def test_username_less_3_chars(self):
        """tests returns error if username less then 3 characters."""
        response = self.client.post(
            "api/v1/auth/register", data=json.dumps(
                dict(
                    first_name="blank",
                    last_name="username",
                    username="us",
                    email="blank@gmail.com",
                    password="@Password2")),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("3-15 alpha-numeric", response_msg["Message"])

    def test_missing_email(self):
        """Tests returns error if email is missing."""
        response = self.client.post(
            "api/v1/auth/register", data=json.dumps(
                dict(
                    first_name="blank",
                    last_name="email",
                    username="blankemail",
                    email="",
                    password="$Uasswor4d")),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("valid email", response_msg["Message"])

    def test_missing_password(self):
        """Tests error raised when password is missing."""
        response = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(
                dict(
                    first_name="first",
                    last_name="last",
                    username="testusername",
                    email="firstlast@gmail.com",
                    password="",
                )),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("6-20 chars", response_msg["Message"])

    def test_username_has_space(self):
        """Tests error raised when username contains spaces."""
        response = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(
                dict(
                    first_name="first",
                    last_name="last",
                    username="first last",
                    email="firstlast@gmail.com",
                    password="#testpassD3"
                )),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("a-zA-Z_.-", response_msg["Message"])

    def test_missing_first_or_last_name(self):
        """Tests error raised when first name or last name is missing."""
        response = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(
                dict(
                    first_name="",
                    last_name="",
                    username="testusername",
                    email="testusername@gmail.com",
                    password="&tD5estpassword"
                )),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("can only be 2-15", response_msg["Message"])

    def test_username_isstring(self):
        """Tests error raised when wrong username format is provided."""
        response = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(
                dict(
                    first_name="first",
                    last_name="last",
                    username=1234,
                    email="firstlast@gmail.com",
                    password="Y3#estpass"
                )),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Wrong", response_msg["Message"])

    def test_duplicate_users(self):
        """
        Tests for duplicate usernames
        """
        response = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(
                dict(
                    first_name="Justin",
                    last_name="Ndwiga",
                    username="justin.ndwiga",
                    email="ndwigatest@gmail.com",
                    password="!passWord3"
                )),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("already exists", response_msg["Message"])

    def test_user_can_register(self):
        """Test new user can be added to the system."""
        response = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(
                dict(
                    first_name="Elon",
                    last_name="Musk",
                    username="elon.musk",
                    email="elon.musk@gmail.com",
                    password="@Yassword5"
                )),
            content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("registered", response_msg["Message"])

    def test_missing_credentials(self):
        """Tests error raised for missing auth details."""
        response = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps(
                dict(
                    username="",
                    password="")),
            content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Username and password", response_msg["Message"])

    def test_unkown_username_login(self):
        """Tests unauthorized error raised with invalid username."""
        response = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps(
                dict(
                    username="invalid",
                    password="testinvalid")),
            content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_invalid_password_login(self):
        """Tests unauthorized error raised with invalid password."""
        response = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps(
                dict(
                    username="justin.ndwiga",
                    password="invalid")),
            content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("invalid", response_msg["Message"])

    def test_valid_login_generates_token(self):
        """Tests token is generated on successful login."""
        response = self.client.post("/api/v1/auth/login",
                                    data=json.dumps(self.user),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("token", response_msg)

    # to be implemented later
    # def test_logout(self):
    #     """Test logout success"""
    #     response = self.client.delete(
    #         '/api/v1/auth/logout',
    #         headers={
    #             "x-access-token": self.token})
    #     self.assertEqual(response.status_code, 200)
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     self.assertIn("out", response_msg["Message"])


if __name__ == "__main__":
    unittest.main()
