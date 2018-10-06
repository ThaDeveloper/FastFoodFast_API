"""Menu endpoints"""
from datetime import datetime
from flask import request, jsonify, Blueprint

# #Local imports
from app.v2.database import Database
from app.v2.models.menu import Menu
from .. utils.authentication import Auth
from ...shared.validation import ValidationError


MENU_V2 = Blueprint('v2_menu', __name__)
DB = Database()
CUR = DB.cursor()
MENU = Menu()


@MENU_V2.route('', methods=['POST'])
@Auth.token_required
def add_menu(current_user):
    """Add Menu item
    Current user must be admin"""
    data = request.get_json()
    try:
        menu_inst = Menu(
            data['name'],
            data['price'],
            data['image'],
            data['category'])
    except KeyError as e:
        return jsonify({"Message": str(e) + "field is missing"}), 500
    try:
        sanitized = menu_inst.import_data(data)
        if sanitized == "Invalid":
            return jsonify(
                {'Message': 'Menu name/price/category cannot be empty'}), 400
    except ValidationError as e:
        return jsonify({"Message": str(e)}), 400
    if current_user['admin']:
        try:
            success = menu_inst.save_menu()
            if not success:
                raise ValueError
            return jsonify({'Message': 'Menu added'}), 201
        except ValueError:
            return jsonify({"Message": "Menu already exists"}), 400
    return jsonify({"Message": "Not authorized to add menu"}), 401


@MENU_V2.route('', methods=['GET'])
def get_full_menu():
    """Get the full list of availabe menu"""
    query = "SELECT * FROM menu"
    CUR.execute(query)
    menus = CUR.fetchall()
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
    return jsonify({"Message": "No Menu found"}), 200


@MENU_V2.route('/<int:item_id>', methods=['GET'])
def get_single_menu_item(item_id):
    """Return specific item by id"""
    item = MENU.get_item_by_id(item_id)
    if item:
        return jsonify({
            'Item': [
                {
                    'id': item['item_id'],
                    'name': item['name'],
                    'price': '%.*f' % (2, item['price']),
                    'category': item['category'],
                    'created_at': item['created_at'],
                    'updated_at': item['updated_at']
                }
            ]
        }), 200
    return jsonify({"Message": "Meal item not found"}), 404


@MENU_V2.route('/<int:item_id>', methods=['PUT'])
@Auth.token_required
def edit_menu_item(current_user, item_id):
    """edit item by specified id"""
    data = request.get_json()
    new_time = datetime.now()
    if current_user['admin']:
        try:
            response = MENU.edit_menu(
                item_id,
                data['name'],
                data['price'],
                data['category'],
                data['image'],
                new_time)
        except KeyError as e:
            return jsonify(str(e) + " field is missing"), 500
        if response == "exists":
            return jsonify({"Message": "Item name exists"}), 400
        if response:
            return jsonify({"Message": "Menu updated"}), 201
        return jsonify({"Message":"Meal item not found"}), 404
    return jsonify({"Message": "Not authorized to edit menu"}), 401

@MENU_V2.route('/<int:item_id>', methods=['DELETE'])
@Auth.token_required
def delete_menu_item(current_user, item_id):
    """Delete Menu by specific id"""
    if current_user['admin']:
        response = MENU.del_menu(item_id)
        if response:
            return jsonify({"Message": "Menu deleted"}), 200
        return jsonify({"Message": "Meal item not found"}), 404
    return jsonify({"Message": "Not authorized to delete menu"}), 401
