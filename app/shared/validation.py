from flask import jsonify
from validate_email import validate_email
import re


class ValidationError(ValueError):
    pass


def validate_user(data):
    username = data['username']
    if not isinstance(username, str):
        return jsonify({"Message":
                        "Wrong username format: Can only be\
                         a string"}), 400
    elif not  re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])"
    "(?=.*[@#$%^&+=*]).{6,}$",data['password']):
        return jsonify({"Message":
                        "Password must be 6-20 chars long:"
                        "Must contain capital,number and special char"}), 400
    elif not  re.match("^[a-zA-Z_.-]{3,15}$", username):
        return jsonify({"Message":
                        "Username must be a commbination of 3-15 letters plus special"
                        " chars (a-zA-Z_.-)"}), 400
    elif not(validate_email(data["email"])):
        return jsonify({'Message':
                        'Enter a valid email'}), 400
    elif not  re.match("^[a-zA-Z]{2,15}$", data['first_name'])\
     or not re.match("^[a-zA-Z]{2,15}$", data['last_name']):
        return jsonify({"Message":
                        "Name can only be 2-15 letters"}), 400
    else:
        True
