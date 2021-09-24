from flask_app.config.mysqlconnection import query_db
from flask import Flask, flash, session
from flask_app.models import arrangement
import datetime
app = Flask(__name__)

class CartItem:
    def __init__(self, data):
        self.id = data['id']
        self.quantity = data['quantity']
        self.cart_id = data['cart_id']
        self.arrangement_id = data['arrangement_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __eq__(self, other):
        return self.id == other.id

    @property
    def arrangement(self):
        query = f"SELECT * FROM arrangements join cart_items on arrangements.id = cart_items.arrangement_id where cart_items.id = {self.id};"
        results = query_db(query)
        arrangement1 = arrangement.Arrangement(results[0])
        return arrangement1

    @property
    def guest_arrangement(self):
        query = f"SELECT * FROM arrangements WHERE arrangements.id = {self.arrangement_id};"
        results = query_db(query)
        arrangement1 = arrangement.Arrangement(results[0])
        return arrangement1

    @classmethod
    def select(cls, type='cart_id', data=None):
        if data:
            query = f"SELECT * FROM cart_items WHERE cart_items.{type} = %({type})s;"
            results = query_db(query, data)
            cart_items = []
            for cart_item in results:
                cart_items.append(cls(cart_item))
            return cart_items
        else:
            query = "SELECT * FROM cart_items;"
            results = query_db(query)
            cart_items = []
            for cart_item in results:
                cart_items.append(cls(cart_item))
            return cart_items

    @classmethod
    def select_one(cls, data, type='arrangement_id'):
        query = f"SELECT * FROM cart_items WHERE cart_items.{type} = %({type})s;"
        results = query_db(query, data)
        if results:
            cart_item = cls(results[0])
            return cart_item
        else:
            return False

    @classmethod
    def create_cart_item(cls, data):
        query = "INSERT INTO cart_items (quantity, cart_id, arrangement_id) VALUES (%(quantity)s, %(cart_id)s, %(arrangement_id)s);"
        results =  query_db(query, data)
        return results

    @classmethod
    def create_guest_cart_item(cls, data):
        data = {
            'id': 2,
            'quantity': data['quantity'],
            'cart_id': 2,
            'arrangement_id': data['id'],
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }
        cart_item = cls(data)
        return cart_item

    @classmethod
    def edit_cart_quantity(cls, data):
        query = "UPDATE cart_items SET quantity = %(quantity)s WHERE cart_items.id = %(id)s;"
        results = query_db(query, data)
        return results

    @classmethod
    def delete_cart_item(cls, data):
        query = "DELETE FROM cart_items WHERE cart_items.id = %(id)s;"
        return query_db(query, data)

    @classmethod
    def delete_cart_items(cls, data):
        query = "DELETE FROM cart_items WHERE cart_items.cart_id = %(cart_id)s;"
        return query_db(query, data)