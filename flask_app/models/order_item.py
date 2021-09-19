from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
from flask_app.models.order import Order
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
        query1 = "select * from cart_items where cart_items.cart_id = %(cart_id)s"
        results1 = connectToMySQL(DATABASE).query_db(query1, data)
        order_data = "%(user_id)s"
        Order.create_order(type='user_id', order_data=order_data)

#STUFF MISSINGF STILLL

        query2 = "INSERT INTO order_items (quantity, order_id, arrangement_id) VALUES (%(quantity)s, %(order_id)s, %(arrangement_id)s"
        results2 =  connectToMySQL(DATABASE).query_db(query2, data)
        return results2

    @classmethod
    def edit_order_item(cls, data):
        query = "UPDATE order_items SET quantity = %(quantity)s, order_id = %(order_id)s, arrangement_id = %(arrangement_id)s WHERE order_items.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    @classmethod
    def delete_order_item(cls, data):
        query = "DELETE FROM order_items WHERE order_items.id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)