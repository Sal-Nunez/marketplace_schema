from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.cart_item import CartItem
from flask_app.models import cart, user

# Use this route to view cart. If guest, use session['cart'] on html side.
@app.route('/cart')
def view_cart():
    if 'uuid' in session:
        data = {
            'user_id': session['uuid']
        }
        user_data = {
            'id':session['uuid']
        }
        carts = cart.Cart.select(data)
        user1 = user.User.select(data = user_data)
        return render_template('view_cart.html', cart = carts, user = user1)
    else:
        return render_template('view_cart.html')

# Takes as input the cart_id, arrangement_id, and quantity
@app.route('/carts/add_arrangement', methods=['POST'])
def add_to_cart():
    if session['uuid']:
        user1 = user.User.select(data={'id':session['uuid']})
        data = {
            'quantity': request.form['quantity'],
            #can get cart from session cart or uuid
            'cart_id': user1.cart.id,
            'arrangement_id': request.form['arrangement_id']
        }
        CartItem.create_cart_item(data)
        return redirect('/cart')
    else:
        if request.form['arrangement_id'] in session['cart']:
            session['cart']['arrangement_id'] = int(request.form['quantity'])
        else:
            session['cart'] = {request.form['arrangement_id']: int(request.form['quantity'])}
    return redirect('/cart') # redirect to current page

# Takes as input the cart_item "id" and cart_item "user_id" and arrangement_id, assume a hidden input
@app.route('/carts/remove_arrangement', methods=['POST'])
def remove_from_cart():
    if session['uuid']:
        if request.form['user_id'] == session['uuid']:
            data = {
                'cart_items.id': request.form['id']
            }
            CartItem.delete_cart_item(data)
    else:
        session['cart'].pop(f"{request.form['arrangement_id']}")

# Takes as input cart_item "id", cart_item "user", qauntity, and arrangement_id, assume a hidden input
@app.route('/carts/update_cart', methods=['POST'])
def update_cart():
    if session['uuid']:
        if request.form['user_id'] == session['uuid']:
            data = {
                'id': request.form['id'],
                'quantity': request.form['quantity']
            }
            CartItem.edit_cart_quantity(data)
    else:
        session['cart']['arrangement_id'] = session['quantity']