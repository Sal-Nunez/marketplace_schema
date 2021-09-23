from flask_app.config.mysqlconnection import query_db
from flask import Flask, flash, session
from flask_app.models import user
from flask_app.models import cart
from flask_app.models import cart_item
from flask_app.models.order_item import OrderItem
app = Flask(__name__)

class Order:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __eq__(self, other):
        return self.id == other.id

    @property
    def order_items(self):
        data = {
            'order_id': self.id
        }
        order_items = OrderItem.select(data)
        return order_items

    @classmethod
    def select(cls, type='email', data=None):
        if data:
            query = f"SELECT * FROM orders WHERE orders.{type} = %({type})s;"
            results = query_db(query, data)
            if results:
                order = cls(results[0])
                return order
            else: return False
        else:
            query = "SELECT * FROM orders;"
            results = query_db(query)
            orders = []
            for order in results:
                orders.append(cls(order))
            return orders

    @classmethod
    def new_order(cls):
        if 'uuid' in session:
            user_data = {
                'user_id': session['uuid']
            }
            cart1 = cart.Cart.select(data=user_data)
            order_id = cls.create_order(data = user_data)
            for item in cart1.cart_items:
                order_item_data = {
                    'quantity': item['quantity'],
                    'arrangement_id': item['arrangement_id'],
                    'order_id': order_id
                }
                OrderItem.create_order_item(data=order_item_data)
            cart_data = {
                'cart_id': cart1.id
            }
            cart_item.CartItem.delete_cart_items(data=cart_data)
            return order_id
        else:
            guest_data = {
                'user_id': 2
            }
            cart.Cart.select(data=guest_data)
            order_id = cls.create_order(data=guest_data)
            for key, value in session['cart']:
                order_item_data = {
                    'arrangement_id': key,
                    'quantity': value,
                    'order_id': order_id
                }
                OrderItem.create_order_item(data = order_item_data)
            session.pop('cart')
            return order_id

    @classmethod
    def create_order(cls, data):
        query = "INSERT into orders (user_id, email) VALUES (%(user_id)s, %(email)s);"
        results =  query_db(query, data)
        return results

# Orders should be treated as immutable and undeletable.
    # @classmethod
    # def delete_order(cls, data, type='id'):
    #     query = f"DELETE FROM orders WHERE orders.{type} = %({type})s;"
    #     return query_db(query, data)