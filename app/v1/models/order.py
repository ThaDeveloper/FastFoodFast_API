from menu import Menu


class Order(Menu):
    """constructor and methods for the Order model"""
    def __init__(self):
        self.orders = {}
    
    def create_order(self, owner, items, servings, status='pending'):
        """Adds a new order to the orders dictionary"""
        new_order = {'order_id': len(self.orders) + 1,
                    'owner': owner,
                    'items': items,
                    'servings': servings,
                    'total': Menu.get_item_price(items) * servings,
                    'status': status}
        self.orders[owner] = new_order
        return self.orders

    def find_order_by_id(self, order_id):
        """Update the staus of an order"""
        if self.orders:
            for order in self.orders.values():
                if order.get('order_id') == order_id:
                    return order
    
    def update_order(self, order_id, status):
        order = self.find_order_by_id(order_id)
        if order:
            order['status'] == status
            return order
    
    def delete_order(self,order_id):
        order = self.find_order_by_id(order_id)
        if order:
            if order['status'] == 'decline':
                del self.orders[order_id]
                return self.orders