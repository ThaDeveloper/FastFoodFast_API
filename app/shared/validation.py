
"""User validation module"""
import re
from flask import jsonify


class ValidationError(ValueError):
    """Base custom validation class for data serializing"""
    pass

def validate_user(data):
    """serializes user inputs and validates correct input"""
    username = str(data["username"]).strip(" ").lower()
    if not isinstance(username, str):
        return jsonify({"Message":
                        "Wrong username format: Can only be"
                            "a string"}), 400
    if not re.match(r"^(?=.*[a-z])[a-zA-Z0-9_.-]{3,15}$", username):
        return jsonify(
            {
                "Message": "Username can only be 3-15 letters or combination of letters,"
                "numbers and _-."}), 400
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])"
                    "(?=.*[@#$%^&+=*!]).{6,}$", data['password']):
        return jsonify({"Message":
                        "Password must be 6-20 chars long:"
                        "Must contain capital,number and special char"}), 400
    if not re.match(r"^[\w.-]+@([\w-]+)\.+\w{2,}$", str(data['email']).strip(" ").lower()):
        return jsonify({'Message':
                        'Enter a valid email'}), 400
    if not re.match(r"^[a-zA-Z]{2,15}$", str(data['first_name']).strip(" ").lower())\
            or not re.match("^[a-zA-Z]{2,15}$", str(data['last_name']).strip(" ").lower()):
        return jsonify({"Message":
                        "Name can only be 2-15 letters"}), 400
