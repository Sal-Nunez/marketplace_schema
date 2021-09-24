from flask_app.config.mysqlconnection import query_db
from flask import Flask, flash, session
from flask_app.models import arrangement
from flask_app.models.category import Category
app = Flask(__name__)

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
    def categories(self):
        query = f"SELECT * FROM categories join product_category on categories.id = product_category.category_id join products on product_category.product_id = products.id WHERE products.id = {self.id};"
        results = query_db(query)
        categories = []
        for category in results:
            data = {
                'id': category['id'],
                'category': category['category'],
                'created_at': category['created_at'],
                'updated_at': category['updated_at']
            }
            categories.append(Category(data))
        return categories

    @property
    def arrangements(self):
        query = f"SELECT * FROM arrangements where arrangements.product_id = {self.id};"
        results = query_db(query)
        arrangements = []
        for arrangement1 in results:
            data = {
                'id': arrangement1['id'],
                'size': arrangement1['size'],
                'price': arrangement1['price'],
                'inventory': arrangement1['inventory'],
                'sale_price': arrangement1['sale_price'],
                'product_id': self.id,
                'created_at': arrangement1['created_at'],
                'updated_at': arrangement1['updated_at']
            }
            arrangements.append(arrangement.Arrangement(data))
        return arrangements

    @classmethod
    def select(cls, type='id', data=None):
        if data:
            query = f"SELECT * FROM products WHERE products.{type} = %({type})s;"
            results = query_db(query, data)
            product = cls(results[0])
            return product
        else:
            query = "SELECT * FROM products;"
            results = query_db(query)
            products = []
            for product in results:
                products.append(cls(product))
            return products
#notdone
    @classmethod
    def search_products(cls, data):
        '''
        data = {
            'name': name + '%'
        }
        '''
        print(f"{'data':*^30}")
        query = "SELECT * FROM products WHERE name LIKE %(name)s LIMIT 6;"
        results = query_db(query, data)
        products = []
        if results:
            for product in results:
                products.append(product.name)
            return products
        else:
            return False

    @classmethod
    def create_product(cls, data):
        query = "INSERT INTO products (name, description, on_sale) VALUES (%(name)s, %(description)s, %(on_sale)s);"
        results =  query_db(query, data)
        return results

    @classmethod
    def edit_product(cls, data):
        query = "UPDATE products SET name = %(name)s, description = %(description)s, on_sale = %(on_sale)s WHERE products.id = %(id)s;"
        results = query_db(query, data)
        return results

    @classmethod
    def delete_product(cls, data):
        query = "DELETE FROM products WHERE products.id = %(id)s;"
        return query_db(query, data)

# The shop owners can name their products whatever they want.
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