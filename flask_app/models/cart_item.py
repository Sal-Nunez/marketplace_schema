from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
from flask_app.models import arrangement
app = Flask(__name__)
DATABASE = "floral_schema"

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
        query = f"SELECT * FROM arrangements join cart_items on arragements.id = cart_item.arrangement_id where carts.id = {self.id}"
        results = connectToMySQL(DATABASE).query_db(query)
        arrangement1 = arrangement.Arrangement(results[0])
        return arrangement1

    @classmethod
    def select(cls, type='cart_id', data=None):
        if data:
            query = f"SELECT * FROM cart_items WHERE cart_items.{type} = %({type})s;"
            results = connectToMySQL(DATABASE).query_db(query, data)
            cart_items = []
            for cart_item in results:
                cart_items.append(cls(cart_item))
            return cart_items
        else:
            query = "SELECT * FROM cart_items;"
            results = connectToMySQL(DATABASE).query_db(query)
            cart_items = []
            for cart_item in results:
                cart_items.append(cls(cart_item))
            return cart_items

    @classmethod
    def create_cart_item(cls, data):
        query = "INSERT INTO cart_items (quantity, cart_id, arrangement_id) VALUES (%(quantity)s, %(cart_id)s, %(arrangement_id)s);"
        results =  connectToMySQL(DATABASE).query_db(query, data)
        return results

    @classmethod
    def edit_cart_quantity(cls, data):
        query = "UPDATE cart_items SET quantity = %(quantity)s WHERE cart_items.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    @classmethod
    def delete_cart_item(cls, data):
        query = "DELETE FROM cart_items WHERE cart_items.id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_cart_items(cls, data):
        query = "DELETE FROM cart_items WHERE cart_items.cart_id = %(cart_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)