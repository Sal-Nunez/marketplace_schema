from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
from flask_app.models.user import User
app = Flask(__name__)
DATABASE = "floral_schema"

class Cart:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']

    def __eq__(self, other):
        return self.id == other.id

    @property
    def owner(self):
        query = f"SELECT * FROM carts WHERE carts.user_id = {self.id}"
        results = connectToMySQL(DATABASE).query_db(query)
        owner = User(results[0])
        return owner

    @classmethod
    def select(cls, data=None, type='user_id'):
        if data:
            query = f"SELECT * FROM carts WHERE carts.{type} = %({type})s"
            results = connectToMySQL(DATABASE).query_db(query, data)
            cart = cls(results[0])
            return cart
        else:
            query = "SELECT * FROM carts"
            results = connectToMySQL(DATABASE).query_db(query)
            carts = []
            for cart in results:
                carts.append(cls(cart))
            return carts

    @classmethod
    def create_cart(cls, data):
        query = "INSERT INTO carts (user_id) VALUES (%(user_id)s)"
        results =  connectToMySQL(DATABASE).query_db(query, data)
        return results


    @classmethod
    def delete_cart(cls, data, type='id'):
        query = f"DELETE FROM carts WHERE carts.{type} = %({type})s"
        return connectToMySQL(DATABASE).query_db(query, data)