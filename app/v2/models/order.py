"""order module"""
from datetime import datetime
from decimal import Decimal
from flask import json

from .menu import Menu
from .. database import Database
from ...shared.validation import ValidationError

DB = Database()


class Order:
    """constructor and methods for the Order model"""

    def __init__(self, user_id=1, items={}, total=0.00, status='New'):
        self.user_id = user_id
        self.items = items
        self.total = total
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.CUR = DB.cursor()

    def create_order(self):
        """Save an order to db"""
        try:
            query = "INSERT INTO orders(user_id,items, total,status,created_at, updated_at)\
            VALUES(%s,%s,%s,%s,%s,%s)"
            self.CUR.execute(
                query,
                (self.user_id,
                 json.dumps(self.items),
                 self.total,
                 self.status,
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
            if type(data['items']) != dict or len(data['items']) == 0:
                return "Invalid"
            for item in data['items']:
                if len(item) == 0:
                    return "Invalid"
            else:
                self.items = data['items']
        except KeyError as e:
            raise ValidationError("Invalid: Field required: " + e.args[0])
        return self

    def find_order_by_id(self, order_id):
        """Find an order by specific id"""
        query = "SELECT * FROM orders WHERE order_id=%s"
        self.CUR.execute(query, (order_id,))
        row = self.CUR.fetchone()
        if row:
            return row
        return False

    def edit_order(
            self,
            order_id,
            items,
            total,
            updated_at):
        """Update order items"""
        query = "UPDATE orders SET items=%s, total=%s, updated_at=%s WHERE order_id=%s"
        self.CUR.execute(query, (json.dumps(items), total, updated_at, order_id))
        DB.connection.commit()
        return True

    def update_order_status(
            self,
            order_id,
            status,
            updated_at):
        """updates the status of a given order"""
        query = "UPDATE orders SET status=%s, updated_at=%s WHERE order_id=%s;"
        self.CUR.execute(query, (status, updated_at, order_id))
        DB.connection.commit()
        return True

    def delete_order(
            self,
            order_id):
        """Deletes  a given order"""
        query = "DELETE FROM orders WHERE order_id=%s"
        self.CUR.execute(query, (order_id,))
        DB.connection.commit()
        return True

    def total_cost(self, items):
        """calculate total order cost"""
        total = Decimal(0.00)
        query = "SELECT name FROM menu"
        cur = DB.cursor()
        cur.execute(query)
        full_menu = cur.fetchall()
        foods = []
        missing_foods = []
        for item in full_menu:
            foods.append(item['name'])
        for food, servings in items.items():
            if food not in foods:
                missing_foods.append(food)
            menu_inst = Menu()
            price = menu_inst.get_item_price(food)
            if not isinstance(servings, int):
                return "NaN"
            total += Decimal(price) * servings                    
        return total, missing_foods
