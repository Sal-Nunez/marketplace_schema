from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
app = Flask(__name__)
DATABASE = "floral_schema"

class Order:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']

    def __eq__(self, other):
        return self.id == other.id

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
    def create_order(cls, data):
        query = "INSERT INTO orders (user_id) VALUES (%(user_id)s)"
        results =  connectToMySQL(DATABASE).query_db(query, data)
        return results


    @classmethod
    def delete_order(cls, data, type='id'):
        query = f"DELETE FROM orders WHERE orders.{type} = %({type})s"
        return connectToMySQL(DATABASE).query_db(query, data)