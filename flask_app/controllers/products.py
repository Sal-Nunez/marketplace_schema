from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
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
        return render_template('product.html', **data)
    else:
        data = {
            'product': product.Product.select(type='name', data=product_data)
        }
        return render_template('product.html', **data)

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
        return render_template('products.html', **data)
    else:
        data = {
            'products': product.Product.select()
        }
        return render_template('products.html', **data)
#notdone
@app.route('/search/<string:name>')
def search_dropdown(name):
    print('name*****************************', name)
    msg = {
        'status': 200
    }
    # product_list = {}
    product_data = {
        'name': name+'%'
    }
    print (f"{'product_data':*^40}", product_data['name'])
    products = product.Product.search_products(data=product_data)
    print('products****************************',products)
    if products:
        return jsonify(msg)
    else:
        return jsonify(msg)