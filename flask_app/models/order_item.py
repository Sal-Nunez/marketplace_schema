from flask_app.config.mysqlconnection import query_db
from flask import Flask, flash, session
from flask_app.models.product import Product
from flask_app.models.arrangement import Arrangement
app = Flask(__name__)


class OrderItem:
    def __init__(self, data):
        self.id = data['id']
        self.quantity = data['quantity']
        self.order_id = data['order_id']
        self.arrangement_id = data['arrangement_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __eq__(self, other):
        return self.id == other.id

    @property
    def product(self):
        query = f"SELECT * FROM products join arrangements on products.id = arrangements.product_id join order_items on arrangements.id = order_items.arrangement_id where order_items.id = {self.id};"
        results = query_db(query)
        product = Product(results[0])
        return product

    @property
    def arrangement(self):
        query = f"SELECT * FROM arrangements join order_items on arrangements.id = order_items.arrangement_id WHERE order_items.id = {self.id};"
        results = query_db(query)
        arrangement = Arrangement(results[0])
        return arrangement

    @classmethod
    def select(cls, type='order_id', data=None):
        if data:
            query = f"SELECT * FROM order_items WHERE order_items.{type} = %({type})s;"
            results = query_db(query, data)
            order_items = []
            for order_item in results:
                order_items.append(order_item)
                return order_items
        else:
            query = "SELECT * FROM order_items;"
            results = query_db(query)
            order_items = []
            for order_item in results:
                order_items.append(cls(order_item))
            return order_items

    @classmethod
    def create_order_item(cls, data):
        query = "INSERT INTO order_items (quantity, order_id, arrangement_id) VALUES (%(quantity)s, %(order_id)s, %(arrangement_id)s);"
        results = query_db(query, data)
        return results

# Shouldn't have to use because orders are immutable.
    # @classmethod
    # def edit_order_item(cls, data):
    #     query = "UPDATE order_items SET quantity = %(quantity)s, order_id = %(order_id)s, arrangement_id = %(arrangement_id)s WHERE order_items.id = %(id)s;"
    #     results = query_db(query, data)
    #     return results

# Shouldn't have to use because orders are immutable.
    # @classmethod
    # def delete_order_item(cls, data):
    #     query = "DELETE FROM order_items WHERE order_items.id = %(id)s;"
    #     return query_db(query, data)
