from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
from flask_app.models.order import Order
from flask_app.models.user import User
app = Flask(__name__)
DATABASE = "floral_schema"

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

    @classmethod
    def select(cls, type='order_id', data=None):
        if data:
            query = f"SELECT * FROM order_items WHERE order_items.{type} = %({type})s"
            results = connectToMySQL(DATABASE).query_db(query, data)
            order_item = cls(results[0])
            return order_item
        else:
            query = "SELECT * FROM order_items"
            results = connectToMySQL(DATABASE).query_db(query)
            order_items = []
            for order_item in results:
                order_items.append(cls(order_item))
            return order_items

    @classmethod
    def create_order_item(cls, data):
        user_data = "%(user_id)s"
        # user = User.select(data=user_data)
        query3 = "SELECT * from carts where user_id = %(user_id)s"
        results3 = connectToMySQL(DATABASE).query_db(query3, data)
        cart = cls(results3[0])
        query1 = f"select * from cart_items where cart_items.cart_id = {cart.id}"
        results1 = connectToMySQL(DATABASE).query_db(query1, data)
        order = Order.create_order(data = user_data)
        for item in results1:
            order_item_data = {
                'quantity': item['quantity'],
                'arrangement_id': item['arrangement_id'],
                'order_id': order.id
            }
            query2 = "INSERT INTO order_items (quantity, order_id, arrangement_id) VALUES (%(quantity)s, %(order_id)s, %(arrangement_id)s"
            connectToMySQL(DATABASE).query_db(query2, order_item_data)
        return order

    @classmethod
    def edit_order_item(cls, data):
        query = "UPDATE order_items SET quantity = %(quantity)s, order_id = %(order_id)s, arrangement_id = %(arrangement_id)s WHERE order_items.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    @classmethod
    def delete_order_item(cls, data):
        query = "DELETE FROM order_items WHERE order_items.id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)