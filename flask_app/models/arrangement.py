from flask_app.config.mysqlconnection import query_db
from flask import Flask, flash, session
from flask_app.models import product
app = Flask(__name__)

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

    @property
    def image(self):
        query = f"SELECT * FROM images WHERE arrangement_id = {self.id};"
        results = query_db(query)
        image1 = results[0]
        image = image1['image']
        return image

    @property
    def product(self):
        data = {
            'id': self.product_id
        }
        return product.Product.select(data=data)

    @classmethod
    def select(cls, type='id', data=None):
        if data:
            query = f"SELECT * FROM arrangements WHERE arrangements.{type} = %({type})s;"
            results = query_db(query, data)
            arrangements = []
            for arrangement in results:
                arrangements.append(cls(arrangement))
            return arrangements
        else:
            query = "SELECT * FROM arrangements;"
            results = query_db(query)
            arrangements = []
            for arrangement in results:
                arrangements.append(cls(arrangement))
            return arrangements

    @classmethod
    def select_one(cls, data):
        query = "SELECT * FROM arrangements WHERE arrangements.id = %(id)s;"
        results = query_db(query, data)
        arrangement = cls(results[0])
        return arrangement

    @classmethod
    def select_arrangement_from_product(cls, data):
        query = "SELECT * FROM arrangements JOIN products on arrangements.product_id = products.id WHERE arrangements.size = 'Deluxe' AND products.name = %(name)s"
        results = query_db(query, data)
        if results:
            arrangement = cls(results[0])
            return arrangement
        else:
            return False

    @classmethod
    def create_arrangement(cls, data):
        query = "INSERT INTO arrangements (size, price, inventory, sale_price, product_id) VALUES (%(size)s, %(price)s, %(inventory)s, %(sale_price)s, %(product_id)s);"
        results =  query_db(query, data)
        return results

    @classmethod
    def edit_arrangement(cls, data):
        query = "UPDATE arrangements SET size = %(size)s, price = %(price)s, inventory = %(inventory, sale_price, product_id)s WHERE arrangements.id = %(id)s;"
        results = query_db(query, data)
        return results

    @classmethod
    def delete_arrangement(cls, data):
        query = "DELETE FROM arrangements WHERE arrangements.id = %(id)s;"
        return query_db(query, data)