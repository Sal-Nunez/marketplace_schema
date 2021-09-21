from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
app = Flask(__name__)
DATABASE = "floral_schema"

class GuestOrderItem:
    def __init__(self, data):
        self.id = data['id']
        self.quantity = data['quantity']
        self.guest_order_id = data['guest_order_id']
        self.arrangement_id = data['arrangement_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    def select(cls, type='guest_order_id', data=None):
        if data:
            query = f"SELECT * FROM guest_order_items WHERE guest_order_items.{type} = %({type})s;"
            results = connectToMySQL(DATABASE).query_db(query, data)
            guest_order_item = cls(results[0])
            return guest_order_item
        else:
            query = "SELECT * FROM guest_order_items;"
            results = connectToMySQL(DATABASE).query_db(query)
            guest_order_items = []
            for guest_order_item in results:
                guest_order_items.append(cls(guest_order_item))
            return guest_order_items
    
    @classmethod
    def create_guest_order_item(cls, data):
        query = "INSERT INTO quest_order_items (quantity, guest_order_id, arrangement_id) VALUES (%(quantity)s, %(guest_order_id)s, %(arrangement_id)s);"
        results =  connectToMySQL(DATABASE).query_db(query, data)
        guest_order_item = cls(results[0])
        return guest_order_item