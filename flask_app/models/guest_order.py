from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
from flask_app.models.guest_order_item import GuestOrderItem
app = Flask(__name__)
DATABASE = "floral_schema"

class GuestOrder:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']

    @property
    def guest_order_items(self):
        guest_order_items = []
        data = {
            'guest_order_id': self.id
        }
        guest_order_item = GuestOrderItem.select(data)
        guest_order_items.append(guest_order_item)
        return guest_order_items
    

    @classmethod
    def select(cls, data=None, type='email'):
        if data:
            query = f"SELECT * FROM guest_orders WHERE guest_orders.{type} = %({type})s;"
            results = connectToMySQL(DATABASE).query_db(query, data)
            guest_order = cls(results[0])
            return guest_order
        else:
            query = "SELECT * FROM guest_orders;"
            results = connectToMySQL(DATABASE).query_db(query)
            guest_orders = []
            for guest_order in results:
                guest_orders.append(cls(guest_order))
            return guest_orders

    @classmethod
    def create_guest_order(cls, data):
        query = "Insert into guest_orders (email) VALUES (%(email)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # Takes in the guest account email, needs to generate an order with an order list, the orderlist will take from session['cart']
    @classmethod
    def new_guest_order(cls):
        guest_order = cls(cls.select(data = {'id': cls.create_guest_order(data={'email': session['email']})}))
        guest_order.guest_order_items = []
        for arrangement_id, quantity in session['cart']:
            data = {
                'arrangement_id': arrangement_id,
                'quantity': quantity,
                'guest_order_id': guest_order.id
            }
            guest_order_item = GuestOrderItem.select(data)
            guest_order.guest_order_items.append(guest_order_item)
        return guest_order