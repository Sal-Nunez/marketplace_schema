from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
from flask_app.models.arrangement import Arrangement
app = Flask(__name__)
DATABASE = "floral_schema"

class Product:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.on_sale = data['on_sale']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __eq__(self, other):
        return self.id == other.id

    @property
    def arrangements(self):
        query = f"SELECT * FROM arrangements where arrangements.product_id = {self.id}"
        results = connectToMySQL(DATABASE).query_db(query)
        arrangements = []
        for arrangement in results:
            data = {
                'id': arrangement['id'],
                'size': arrangement['size'],
                'price': arrangement['price'],
                'inventory': arrangement['inventory'],
                'sale_price': arrangement['sale_price']
            }
            arrangements.append(Arrangement(data))
        return arrangements

    @classmethod
    def select(cls, type='id', data=None):
        if data:
            query = f"SELECT * FROM products WHERE products.{type} = %({type})s"
            results = connectToMySQL(DATABASE).query_db(query, data)
            product = cls(results[0])
            return product
        else:
            query = "SELECT * FROM products"
            results = connectToMySQL(DATABASE).query_db(query)
            products = []
            for product in results:
                products.append(cls(product))
            return products

    @classmethod
    def create_product(cls, data):
        query = "INSERT INTO products (name, description, on_sale) VALUES (%(name)s, %(description)s, %(on_sale)s)"
        results =  connectToMySQL(DATABASE).query_db(query, data)
        return results

    @classmethod
    def edit_product(cls, data):
        query = "UPDATE products SET name = %(name)s, description = %(description)s, on_sale = %(on_sale)s WHERE products.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    @classmethod
    def delete_product(cls, data):
        query = "DELETE FROM products WHERE products.id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)


    # @classmethod
    # def validate_product_info(cls, data):
    #     is_valid = True
    #     if len(data['name']) < 2:
    #         flash("name must be at least two characters", "name")
    #         is_valid = False
    #     if len(data['description']) < 10:
    #         flash("description must be at least 10 characters", "description")
    #         is_valid = False
    #     return is_valid