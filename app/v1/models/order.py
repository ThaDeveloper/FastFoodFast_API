import datetime
from .menu import Menu
from ...shared.validation import ValidationError


class Order:
    """constructor and methods for the Order model"""

    def __init__(self):
        self.orders = {}

    def create_order(
            self,
            user_id,
            items={
                "item": 0},
            total=0,
            status='pending'):
        """Adds a new order to the orders dictionary"""
        if not self.orders:
            order_id = 1
        else:
            order_id = list(self.orders.keys())[-1] + 1
        new_order = {'order_id': order_id,
                     'user_id': user_id,
                     'items': items,
                     'total': total,
                     'status': status,
                     'created_at': datetime.datetime.now()}

        self.orders[order_id] = new_order
        return self.orders

    def find_order_by_id(self, order_id):
        """Find an order by specific id"""
        if self.orders:
            for order in self.orders.values():
                if order.get('order_id') == order_id:
                    return order

    def update_order(
            self,
            order_id,
            status,
            updated_at=datetime.datetime.now()):
        """Update the status of an order"""
        order = self.find_order_by_id(order_id)
        if order:
            order['status'] = status
            order['updated_at'] = updated_at
            return order

    def cancel_order(self, order_id):
        order = self.find_order_by_id(order_id)
        if order:
            del self.orders[order['order_id']]

    def import_data(self, data):
        """validates the input json data"""
        try:
            if len(data['items']) == 0:
                return "Invalid"
            else:
                self.items = data['items']
        except KeyError as e:
            raise ValidationError("Invalid: Field required: " + e.args[0])
        return self

    @staticmethod
    def total_cost(items):
        total = 0
        menu_inst = Menu()
        for food, servings in items.items():
            price = menu_inst.get_item_price(food)
            total += price * servings
        return total
