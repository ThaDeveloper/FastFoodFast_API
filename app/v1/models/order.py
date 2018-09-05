import datetime
from .menu import Menu


class Order:
    """constructor and methods for the Order model"""

    def __init__(self):
        self.orders = {}

    def create_order(
            self,
            owner,
            items={
                "item": 0},
            total=0,
            status='pending'):
        """Adds a new order to the orders dictionary"""
        new_order = {'order_id': len(self.orders) + 1,
                     'owner': owner,
                     'items': items,
                     'total': total,
                     'status': status,
                     'created_at': datetime.datetime.now()}
        self.orders[owner] = new_order
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
            del self.orders[order['owner']]

    @staticmethod
    def total_cost(items):
        total = 0
        menu_inst = Menu()
        for food, servings in items.items():
            price = menu_inst.get_item_price(food)
            total += price * servings
        return total
