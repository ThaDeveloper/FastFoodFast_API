import datetime
from flask import jsonify
from ...shared.validation import ValidationError


class Menu:
    def __init__(self):
        """Initialize menu with few items"""
        self.menu = {
            'burger': {
                'item_id': 1,
                'name': 'burger',
                'image': 'burger.jpg',
                'price': 800,
                'category': 'snacks'},
            'pizza': {
                'item_id': 2,
                'name': 'pizza',
                'image': 'pizza.jpg',
                'price': 1000,
                'category': 'snacks'}
            }

    def get_item_price(self, item):
        """Find price of a menu item by passing item name"""
        if self.menu:
            if item in self.menu:
                return self.menu[item]['price']

    def add_menu(self, name, price, category, image="food.jpg"):
        """Adds new menu item and returns all menus"""
        new_item = {
            'item_id': len(self.menu) + 1,
            'name': name,
            'image': image,
            'price': price,
            'category': category,
            'created_at': datetime.datetime.now()
        }
        self.menu[name] = new_item
        return self.menu

    def import_data(self, data):
        """validates the input json data"""
        try:
            if len(data['name']) == 0 or data['price'] == "":
                return "Invalid"
            else:
                self.name = data['name']
                self.price = data['price']
                self.category = data['category']
                self.image = data['image']
        except KeyError as e:
            raise ValidationError("Invalid: Field required: " + e.args[0])
        return self
    
    def get_item_by_id(self, item_id):
        """Returns a single menu item"""
        for item in self.menu.values():
            if item.get('item_id') == item_id:
                return item