from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import product
from flask_app.models import user, arrangement


@app.route('/products/<string:product_name>', methods=['POST'])
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
            'user': user.User.select(data = id),
            'arrangement': arrangement.Arrangement.select(data={'id':request.form['id']})
        }
        return redirect(f"/products/{product_name}", **data)
    else:
        data = {
            'product': product.Product.select(type='name', data=product_data),
            'arrangement': arrangement.Arrangement.select(data={'id':request.form['id']})
        }
        return redirect(f"/products/{product_name}", **data)

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
    is_valid = True
    # product_list = {}
    product_data = {
        'name': name
    }
    products = product.Product.search_products(data=product_data)
    if products:
        print('products****************************',products)
    else:
        is_valid = False