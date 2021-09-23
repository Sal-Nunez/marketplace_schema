from flask_app.config.mysqlconnection import query_db
from flask import Flask, flash, session
from flask_app.models import user, cart_item
app = Flask(__name__)

class Cart:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __eq__(self, other):
        return self.id == other.id

    @property
    def cart_items(self):
        data = {
            'cart_id': self.id
        }
        cart_items = cart_item.CartItem.select(data=data)
        return cart_items

    @property
    def owner(self):
        query = f"SELECT * FROM users JOIN carts on users.id = carts.user_id WHERE carts.user_id = {self.id};"
        results = query_db(query)
        owner = user.User(results[0])
        return owner

    @classmethod
    def select(cls, data=None, type='user_id'):
        if data:
            query = f"SELECT * FROM carts WHERE carts.{type} = %({type})s;"
            results = query_db(query, data)
            cart = cls(results[0])
            return cart
        else:
            query = "SELECT * FROM carts;"
            results = query_db(query)
            carts = []
            for cart in results:
                carts.append(cls(cart))
            return carts

    @classmethod
    def create_cart(cls, data):
        query = "INSERT INTO carts (user_id) VALUES (%(user_id)s);"
        results = query_db(query, data)
        return results

    @classmethod
    def delete_cart(cls, data, type='id'):
        query = f"DELETE FROM carts WHERE carts.{type} = %({type})s;"
        return query_db(query, data)
