"""menu module"""
from datetime import datetime

#local
from ...shared.validation import ValidationError
from .. database import Database

db = Database()
cur = db.cursor()

class Menu:
    """Menu model to hold menu details"""
    def __init__(self, name="name", price=100.00, image="image.jpg", category="cat"):
        """Menu constructor to initialize menu properties"""
        self.name = name
        self.price = price
        self.image = image
        self.category = category
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.cur = db.cursor()
        
    def check_menu_exists(self, name):
        """Check if menu exists"""
        query = "SELECT name FROM menu WHERE name = '%s'" % (name)
        self.cur.execute(query)
        return self.cur.fetchone() is not None

    def save_menu(self):
        """Adds new menu item and returns all menus"""
        if self.check_menu_exists(self.name):
            return False
        try:
            query = "INSERT INTO menu(name,price,category, image, created_at, updated_at) VALUES(%s,%s,%s,%s,%s,%s)"
            self.cur.execute(query, (self.name, self.price, self.category, self.image, self.created_at, self.updated_at))
            db.connection.commit()
            self.cur.close()
        except ValueError as e:
            return e
        return True

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
        query = "SELECT  * FROM menu WHERE item_id='%s'"
        self.cur.execute(query, (item_id,))
        row = self.cur.fetchone()
        if row:
            return row
        return False

    
    def get_item_price(self, item):
        """Find price of a menu item by passing item name"""
        query = "SELECT price FROM WHERE name='%s'"
        self.cur.execute(query, (item,))
        row = self.cur.fetchone()
        if row:
            self.cur.close()
            return row
        return False

    def edit_menu(
            self,
            item_id,
            name,
            price,
            category,
            image,
            updated_at= datetime.now()):
        item = self.get_item_by_id(item_id)
        if item:
            query = "UPDATE menu SET name='%s', price='%s', category='%s', image='%s', updated_at='%s'"
            self.cur.execute(query, (name, price, category, image, updated_at))
            db.connection.commit()
            self.cur.close()
            return True
        return False

    def del_menu(self, item_id):
        """Delete menu by id"""
        item = self.get_item_by_id(item_id)
        if item:
            query = "DELETE FROM menu WHERE item_id='%s'"
            self.cur.execute(query, (item_id,))
            db.connection.commit()
            self.cur.close()
            return True
        return False
