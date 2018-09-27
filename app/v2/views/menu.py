import os
import datetime
import jwt
from flask import request, jsonify, Blueprint

# #Local imports
from .. utils.authentication import Auth
from ...shared.validation import ValidationError
from app.v2.models.menu import Menu
from app.v2.database import Database

menu_v2 = Blueprint('v2_menu', __name__)
db = Database()
cur = db.cursor()

@menu_v2.route('', methods=['POST'])
@Auth.token_required
def add_menu(current_user):
    data = request.get_json()
    menu_inst = Menu(data['name'], data['price'], data['image'], data['category'])
    try:
        sanitized = menu_inst.import_data(data)
        if sanitized == "Invalid":
            return jsonify(
                {'Message': 'Menu name/price/category cannot be empty'}), 400
    except ValidationError as e:
        return jsonify({"Message": str(e)}), 400
    if current_user['admin']:
        try:
            success= menu_inst.save_menu()
            if not success:
                raise ValueError
            return jsonify({'Message': 'Menu added'}), 201
        except ValueError:
            return jsonify({"Message": "Menu already exists"}), 400
    return jsonify({"Message": "Not authorized to add menu"}), 401

@menu_v2.route('', methods=['GET'])
def get_full_menu():
    query = "SELECT * FROM menu"
    cur.execute(query)
    menus = cur.fetchall()
    if menus:
        return jsonify({
            "Full Menu": [
                {
                    'id': menu['item_id'],
                    'name': menu['name'],
                    'price': '%.*f' % (2, menu['price']),
                    'category': menu['category'],
                    'created_at': menu['created_at'],
                    'updated_at': menu['updated_at']
                } for menu in menus
            ]
            
        }), 200
    return jsonify({"Message": "No menu found"}), 200

