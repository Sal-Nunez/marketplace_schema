from flask_app import app
from flask import render_template, redirect, request, session, flash

@app.route('/products/<str:product_name>')
def one_product(product_name):
    pass