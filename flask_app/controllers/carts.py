from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.cart_item import CartItem
from flask_app.models import cart, user, arrangement

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
        cart_items = []
        for cart_item in session:
            data = {
                'id': cart_item,
                'quantity': session[cart_item]
            }
            cart_item = CartItem.create_guest_cart_item(data)
            cart_items.append(cart_item)
        data1 = {
            'cart_items': cart_items 
        }
        return render_template('view_cart.html', **data1)

# Takes as input the cart_id, arrangement_id, and quantity
@app.route('/carts/add_arrangement', methods=['POST'])
def add_to_cart():
    if 'uuid' in session:
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
        arrangement1 = request.form['arrangement_id']
        if arrangement1 in session:
            session[arrangement1] += int(request.form['quantity'])
        else:
            session[arrangement1] = int(request.form['quantity'])
    return redirect('/cart') # redirect to current page

# Takes as input the cart_item "id" and cart_item "user_id" and arrangement_id, assume a hidden input
@app.route('/carts/remove_arrangement', methods=['POST'])
def remove_from_cart():
    if 'uuid' in session:
        if request.form['user_id'] == session['uuid']:
            data = {
                'id': request.form['id']
            }
            CartItem.delete_cart_item(data)
            return redirect('/cart') # redirect to current page
    else:
        session['cart'].pop(f"{request.form['arrangement_id']}")
        return redirect('/cart') # redirect to current page

# Takes as input cart_item "id", cart_item "user", qauntity, and arrangement_id, assume a hidden input
@app.route('/carts/update_cart', methods=['POST'])
def update_cart():
    if 'uuid' in session:
        if request.form['user_id'] == session['uuid']:
            data = {
                'id': request.form['id'],
                'quantity': request.form['quantity']
            }
            CartItem.edit_cart_quantity(data)
    else:
        session['cart']['arrangement_id'] = session['quantity']

@app.route('/checkout')
def checkout():
    if 'uuid' in session:
        user_data = {
            'id': session['uuid']
        }
        cart_data = {
            'user_id': session['uuid']
        }
        data = {
            'user': user.User.select(data=user_data),
            'cart': cart.Cart.select(data=cart_data)
        }
        return render_template('checkout.html', **data)
    else:
        cart_items = []
        for cart_item in session:
            data = {
                'id': cart_item,
                'quantity': session[cart_item]
            }
            cart_item = CartItem.create_guest_cart_item(data)
            cart_items.append(cart_item)
        data1 = {
            'cart_items': cart_items 
        }
        return render_template('checkout.html', **data1)