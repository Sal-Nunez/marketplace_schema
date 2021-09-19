from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
import re
from flask_bcrypt import Bcrypt
app = Flask(__size__)
bcrypt = Bcrypt(app)
DATABASE = "floral_schema"

class Arrangement:
    def __init__(self, data):
        self.id = data['id']
        self.size = data['size']
        self.price = data['price']
        self.inventory = data['inventory']
        self.sale_price = data['sale_price']
        self.product_id = data['product_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    def select(cls, type='id', data=None):
        if data:
            query = f"SELECT * FROM arrangements WHERE arrangements.{type} = %({type})s"
            results = connectToMySQL(DATABASE).query_db(query, data)
            arrangement = cls(results[0])
            return arrangement
        else:
            query = "SELECT * FROM arrangements"
            results = connectToMySQL(DATABASE).query_db(query)
            arrangements = []
            for arrangement in results:
                arrangements.append(cls(arrangement))
            return arrangements

    @classmethod
    def create_arrangement(cls, data):
        query = "INSERT INTO arrangements (size, price, inventory, sale_price, product_id) VALUES (%(size)s, %(price)s, %(inventory)s, %(sale_price)s, %(product_id)s)"
        results =  connectToMySQL(DATABASE).query_db(query, data)
        return results

    @classmethod
    def edit_arrangement(cls, data):
        query = "UPDATE arrangements SET size = %(size)s, price = %(price)s, inventory = %(inventory, sale_price, product_id)s WHERE arrangements.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    @classmethod
    def delete_arrangement(cls, data):
        query = "DELETE FROM arrangements WHERE arrangements.id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)