from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
app = Flask(__name__)
DATABASE = "floral_schema"

class Category:
    def __init__(self, data):
        self.id = data['id']
        self.category = data['category']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __eq__(self, other):
        return self.id == other.id