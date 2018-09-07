from flask import jsonify
from validate_email import validate_email


class ValidationError(ValueError):
    pass


def validate_user(data):
    if not isinstance(data['username'], str):
        return jsonify({"Message":
                        "Wrong username format: Can only be a string"}), 400
    elif len(data['username'].strip()) == 0 or\
            len(data['password'].strip()) == 0 or\
            len(data['first_name'].strip()) == 0 or\
            len(data['last_name'].strip()) == 0:
        return jsonify({'Message':
                        "All fields are required"}), 400
    elif len(data['username'].strip()) < 3:
        return jsonify({"Message":
                        "Username must be 3 characters and above"}), 400

    elif not(validate_email(data["email"])):
        return jsonify({'Message':
                        'Enter a valid email'}), 400
    else:
        for x in data['username']:
            if x.isspace():
                return jsonify({"Message":
                                "Username can't contain spaces"}), 400
