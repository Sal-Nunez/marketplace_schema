from flask_app.config.mysqlconnection import query_db
from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import product
from flask_app.models import user, arrangement
DATABASE = "floral_schema"

@app.route('/product/<int:id>')
def one_product(id):
    product_id = {
        'id': id
    }
    if 'uuid' in session:
        user_id = {
            'id': session['uuid']
        }
        data = {
            'user': user.User.select(data = user_id),
            'arrangement': arrangement.Arrangement.select_one(data=product_id)
        }
        return render_template('product.html', **data)
    else:
        data = {
            'arrangement': arrangement.Arrangement.select_one(data=product_id)
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
            'arrangements': arrangement.Arrangement.select(type='size', data={'size': 'Deluxe'})
        }
        return render_template('products.html', **data)
    else:
        data = {
            'arrangements': arrangement.Arrangement.select(type='size', data={'size': 'Deluxe'})
        }
        return render_template('products.html', **data)
#notdone
@app.route('/search', methods=['POST'])
def search():
    product_name = request.form['product_name']
    product1 = arrangement.Arrangement.select_arrangement_from_product(data={'name': product_name})
    if product1:
        return redirect(f"/product/{product1.id}")
    else:
        flash(f"There is no product called \"{request.form['product_name']}\"", 'search_error')
        return redirect('/')


@app.route('/api/search/<name>')
def filter_users(name):
    query = "SELECT name FROM products WHERE products.name LIKE %(name)s LIMIT 5;"
    results1 = query_db(query,{"name":"%"+name+"%"})
    # query = "SELECT category FROM categories WHERE categories.category LIKE %(name)s LIMIT 5;"
    # results2 = query_db(query, {"name": "%"+name+"%"})
    # print(results1)
    # result = []
    # results1.extend(results2)
    # for myDict in results1:
    #     if myDict not in result:
    #         result.append(myDict)
    result = []
    for product in results1:
        result.append(product)
    return jsonify(result)