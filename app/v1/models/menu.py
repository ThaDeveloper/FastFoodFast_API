class Menu:
    def __init__(self):
        self.menu = {'burger': 800, 'pizza': 1000, 'coffee': 300,
                     'sausage': 100, 'rice': 500}

    def get_item_price(self, items):
        """Find price of a menu item by passing item name"""
        if self.menu:
            if items in self.menu:
                return self.menu[items]
