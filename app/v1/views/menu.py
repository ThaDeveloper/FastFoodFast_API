from flask import request, jsonify, Blueprint, make_response
import datetime

from ..models.menu import Menu
from ...shared.authentication import Auth
from ...shared.validation import ValidationError

# Blueprint app to handle our menu resources
menu_v1 = Blueprint('menu', __name__)
menu_inst = Menu()
full_menu = menu_inst.menu

@menu_v1.route('', methods=['POST'])
@Auth.token_required
def add_menu(current_user):
    data = request.get_json()
    try:
        sanitized = menu_inst.import_data(data)
        if sanitized == "Invalid":
            return jsonify({'Message': 'Menu name/price/category cannot be empty'}), 400
    except ValidationError as e:
        return jsonify({"Message": str(e)}), 400
    if menu_inst.name in full_menu:
        return jsonify({"Message": "Menu item already exists"}), 400
    menu_inst.add_menu(
        menu_inst.name,
        menu_inst.price,
        menu_inst.category,
        menu_inst.image)
    return jsonify({'Message': 'Menu added'}), 201

@menu_v1.route('', methods=['GET'])
def get_full_menu():
    """Returns full menu to user or admin"""
    return jsonify({"Our Menu": full_menu}), 200

@menu_v1.route('/<int:item_id>', methods=['GET'])
def get_single_item(item_id):
    """Returns sinle item to user or admin"""
    item = menu_inst.get_item_by_id(item_id)
    if item:
        return jsonify({"Item": item}), 200
    return jsonify({"Message": "Item not found"}), 404
 
@menu_v1.route('/<int:item_id>', methods=['PUT'])
@Auth.token_required
def update_menu_item(current_user, item_id):
    data = request.get_json()
    new_time = datetime.datetime.now()
    resp = menu_inst.edit_menu(item_id, data['name'], data['price'], data['category'], data['image'], new_time)
   
    if resp:
        #after updating menu item we also want to update dict keys are
        #represented by item name
        return jsonify({"Message": "Item updated"}), 200
    return jsonify({"Message": "Item not found"}), 404

@menu_v1.route('/<int:item_id>', methods=['DELETE'])
@Auth.token_required
def delete_men_item(current_user, item_id):
    resp = menu_inst.del_menu(item_id)
    if resp:
        return jsonify({"Message": "Item deleted"}), 200
    return jsonify({"Message": "Item not found"}), 404