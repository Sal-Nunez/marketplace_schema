from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
from flask_app.models import user
from flask_app.models import cart
app = Flask(__name__)
DATABASE = "floral_schema"

class Order:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']

    def __eq__(self, other):
        return self.id == other.id

    @property
    def order_items(self):
        pass

    @classmethod
    def select(cls, data=None, type='user_id'):
        if data:
            query = f"SELECT * FROM orders WHERE orders.{type} = %({type})s"
            results = connectToMySQL(DATABASE).query_db(query, data)
            order = cls(results[0])
            return order
        else:
            query = "SELECT * FROM orders"
            results = connectToMySQL(DATABASE).query_db(query)
            orders = []
            for order in results:
                orders.append(cls(order))
            return orders

    @classmethod
    def new_order(cls, data):
        user_data = {
            'user_id': data['user_id']
        }
        cart1 = cart.Cart.select(data=user_data)
        order = cls.create_order(data = user_data)
        for item in cart1.cart_items:
            order_item_data = {
                'quantity': item['quantity'],
                'arrangement_id': item['arrangement_id'],
                'order_id': order.id
            }
            query2 = "INSERT INTO order_items (quantity, order_id, arrangement_id) VALUES (%(quantity)s, %(order_id)s, %(arrangement_id)s"
            connectToMySQL(DATABASE).query_db(query2, order_item_data)
        return order

    @classmethod
    def delete_order(cls, data, type='id'):
        query = f"DELETE FROM orders WHERE orders.{type} = %({type})s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def create_order(cls, data):
        query = "INSERT into orders (user_id) VALUES (%(user_id)s)"
        results =  connectToMySQL(DATABASE).query_db(query, data)
        return results