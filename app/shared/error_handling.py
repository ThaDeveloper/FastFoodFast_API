from flask import jsonify


def page_404(e):
    """Default message returned for missing page"""
    return jsonify({"Message": "Sorry! The page you're looking for is unavailable."}), 404


def bad_request(e):
    """Default message returned for a bad request"""
    return jsonify({"Message":"Oops! Bad request, ensure you send the correct input."}), 400


def method_not_found(e):
    return jsonify({
        "Message": "Something went wrong! The server couldn't intepret the request method, try again."}), 405
