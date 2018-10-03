"""menu module"""
from datetime import datetime
import re
# local
from ...shared.validation import ValidationError
from .. database import Database

DB = Database()


class Menu:
    """Menu model to hold menu details"""

    def __init__(
            self,
            name="name",
            price=100.00,
            image="image.jpg",
            category="cat"):
        """Menu constructor to initialize menu properties"""
        self.name = name
        self.price = price
        self.image = image
        self.category = category
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.CUR = DB.cursor()

    def check_menu_exists(self, name):
        """Check if menu exists"""
        query = "SELECT * FROM menu WHERE name = '%s'" % (name)
        self.CUR.execute(query)
        row = self.CUR.fetchone()
        return row

    def save_menu(self):
        """Adds new menu item and returns all menus"""
        row = self.check_menu_exists(self.name)
        if row:
            return False
        try:
            query = "INSERT INTO menu(name,price,category, image, created_at, updated_at)\
            VALUES(%s,%s,%s,%s,%s,%s)"
            self.CUR.execute(
                query,
                (self.name,
                 self.price,
                 self.category,
                 self.image,
                 self.created_at,
                 self.updated_at))
            DB.connection.commit()
            self.CUR.close()
        except ValueError as e:
            return e
        return True

    def import_data(self, data):
        """validates the input json data"""
        try:
            if not re.match(r"^[a-zA-Z]{4,500}$", data['name']) or\
            not re.match(r"^[a-zA-Z]{4,200}$", data['category'])  or \
            not re.match(r"^[0-9]{4,200}$", data['price']) :
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
        self.CUR.execute(query, (item_id,))
        row = self.CUR.fetchone()
        if row:
            return row
        return False

    def get_item_price(self, item):
        """Find price of a menu item by passing item name"""
        query = "SELECT price FROM menu WHERE name=%s;"
        self.CUR.execute(query, (item,))
        row = self.CUR.fetchone()
        if row:
            return row['price']
        return False

    def edit_menu(
            self,
            item_id,
            name,
            price,
            category,
            image,
            updated_at=datetime.now()):
        """Edit menu by specific"""
        item = self.get_item_by_id(item_id)
        if item:
            row = self.check_menu_exists(name)
            if row and item_id != row['item_id']:
                return "exists"
            query = "UPDATE menu SET name=%s, price=%s, category=%s,\
            image=%s, updated_at=%s WHERE item_id=%s"
            self.CUR.execute(
                query, (name, price, category, image, updated_at, item_id))
            DB.connection.commit()
            return True
        return False

    def del_menu(self, item_id):
        """Delete menu by id"""
        item = self.get_item_by_id(item_id)
        if item:
            query = "DELETE FROM menu WHERE item_id='%s'"
            self.CUR.execute(query, (item_id,))
            DB.connection.commit()
            return True
        return False
