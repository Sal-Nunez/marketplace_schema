from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import product
from flask_app.models import user


@app.route('/products/<string:product_name>')
def one_product(product_name):
    product_data = {
        'name': product_name
    }
    if 'uuid' in session:
        id = {
            'id': session['uuid']
        }
        data = {
            'product': product.Product.select(type='name', data=product_data),
            'user': user.User.select(data = id)
        }
        return render_template('/product.html', **data)
    else:
        data = {
            'product': product.Product.select(type='name', data=product_data)
        }
        return render_template('/product.html', **data)

@app.route('/products/all')
def all_products():
    if 'uuid' in session:
        id = {
            'id': session['uuid']
        }
        data = {
            'user': user.User.select(data=id),
            'products': product.Product.select()
        }
        return render_template('/products', **data)
    else:
        data = {
            'products': product.Product.select()
        }
        return render_template('/products.html', **data)