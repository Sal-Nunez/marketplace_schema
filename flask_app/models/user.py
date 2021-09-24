from flask_app.config.mysqlconnection import query_db
from flask import Flask, flash, session
import re
from flask_bcrypt import Bcrypt
from flask_app.models import order
from flask_app.models import cart, cart_item
app = Flask(__name__)
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]\S*$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __eq__(self, other):
        return self.id == other.id

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def orders(self):
        query = f"SELECT * FROM orders WHERE orders.user_id = {self.id};"
        results = query_db(query)
        orders = []
        for order1 in results:
            orders.append(order.Order(order1))
        return orders

    @property
    def cart(self):
        query = f"SELECT * FROM carts WHERE carts.user_id = {self.id};"
        results = query_db(query)
        cart1 = cart.Cart(results[0])
        return cart1

    @classmethod
    def select(cls, data=None, type='id'):
        if data:
            query = f"SELECT * FROM users WHERE users.{type} = %({type})s;"
            results = query_db(query, data)
            user = cls(results[0])
            return user
        else:
            query = "SELECT * FROM users;"
            results = query_db(query)
            users = []
            for user in results:
                users.append(cls(user))
            return users

    @classmethod
    def check_login(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = query_db(query, data)
        user = cls(results[0])
        if user.email == data['email'] and bcrypt.check_password_hash(user.password, data['password']):
            cart_id = user.cart.id
            for item in session:
                cart_item_data = {
                    'arrangement_id': item,
                    'quantity': session[item],
                    'cart_id': cart_id
                }
                cart_item.CartItem.create_cart_item(data=cart_item_data)
            session.clear()
            session['uuid'] = user.id
            return True
        else:
            return False

    @classmethod
    def registration(cls, data):
        data['password'] = bcrypt.generate_password_hash(data['password'])
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = query_db(query, data)
        user_data = {
            'user_id': results
        }
        if session:
            cart_id = cart.Cart.create_cart(data=user_data)
            for item in session:
                cart_item_data = {
                    'arrangement_id': item,
                    'quantity': session[item],
                    'cart_id': cart_id
                }
                cart_item.CartItem.create_cart_item(data=cart_item_data)
        session.clear()
        if query:
            session['uuid'] = results
        return results