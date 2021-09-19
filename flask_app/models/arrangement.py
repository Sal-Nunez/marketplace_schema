from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
import re
from flask_bcrypt import Bcrypt
app = Flask(__name__)
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