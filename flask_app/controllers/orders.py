from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import order, user

# Once they pay they are taken to this screen, it's their receipt.
# Need to feed to the front a list of all the order items.
    # Need to do this for cart as well.
# Takes in guest email if still not logged in
@app.route('/orders/confirmation', methods=['POST'])
def confirmation():
    if 'uuid' in session:
        orders = order.Order.new_order()
        data = {
            'id': session['uuid']
        }
        users = user.User.select(data)
        return render_template('order_confirmation.html', order = orders, user = users)
    else:
        data = {
            'email': request.form['guest_email']
        }
        orders = order.Order.new_guest_order(data)
        return redirect('order_confirmation.html', order = orders)
