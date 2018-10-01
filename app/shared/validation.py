"""User validation module"""
import re
from flask import jsonify


class ValidationError(ValueError):
    """Base custom validation class for data serializing"""
    pass

def validate_user(data):
    """serializes user inputs and validates correct input"""
    username = data["username"]
    if not isinstance(username, str):
        return jsonify({"Message":
                        "Wrong username format: Can only be"
                            "a string"}), 400
    if not re.match(r"^[a-zA-Z_.-]{3,15}$", username):
        return jsonify(
            {
                "Message": "Username can only be 3-15 letters or combination of letters and _-."
                           " (a-zA-Z_.-)"}), 400
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])"
                    "(?=.*[@#$%^&+=*]).{6,}$", data['password']):
        return jsonify({"Message":
                        "Password must be 6-20 chars long:"
                        "Must contain capital,number and special char"}), 400
    if not re.match(r"^[\w.-]+@([\w-]+)\.+\w{2,}$", data['email']):
        return jsonify({'Message':
                        'Enter a valid email'}), 400
    if not re.match(r"^[a-zA-Z]{2,15}$", data['first_name'])\
            or not re.match("^[a-zA-Z]{2,15}$", data['last_name']):
        return jsonify({"Message":
                        "Name can only be 2-15 letters"}), 400
