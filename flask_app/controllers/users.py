from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

@app.route('/')
def index():
    if 'uuid' in session:
        data = {
            'id': session['uuid']
        }
        user = User.select(data)
        return render_template('index.html', user=user)
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
        msg = {
        'status': 200
        }
        user_email = {
            'email':request.form['email']
        }
        user = User.select(type = 'email', data = user_email)
        is_valid = True
        errors = {}

        if not user:
            errors['user_input_error'] = "Invalid Credentials"
            is_valid = False

        if len(request.form['pw']) < 1:
            errors['login_pw_error'] = "Must input a password"
            is_valid = False

        if user:
            if not bcrypt.check_password_hash(user.pw, request.form['pw']):
                is_valid = False
                errors['user_input_error'] = "Invalid Credentials"

        if not is_valid:
            msg['status'] = 400
            msg['errors'] = errors
            return jsonify(msg)
        
        session['uuid'] = user.id
        return jsonify(msg)


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    else:
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': request.form['password']
        }
        User.registration(data)
    return redirect('/')

@app.route('/account')
def account():
    if not 'uuid' in session:
        return redirect('/')
    else:
        data = {
            'user': User.select(type='id', data={'id': session['uuid']})
        }
        return render_template('account.html', **data)

@app.route('/logout')
def logout():
    session.pop('uuid')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if not 'master' in session:
        return redirect('/')
    else:
        data = {
            'user': User.select('someform of user id')
        }
        return render_template('master.html', **data)
