from flask_app import app
from flask import render_template, redirect, request, session, flash

@app.route('/products/<string:product_name>')
def one_product(product_name):
    pass