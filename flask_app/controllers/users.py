from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash, jsonify
from flask_bcrypt import Bcrypt
DATABASE = "floral_schema"
from flask_app.models.user import User
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]\S*$')

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

@app.route('/register', methods=['POST'])
def login():
        msg = {
        'status': 200
        }
        is_valid = True
        errors = {}
        if not request.form['password_confirmation'] == request.form['password']:
            errors['reg_pw_error'] = 'Passwords Do Not Match'
            is_valid = False
        if not NAME_REGEX.match(request.form['first_name']):
            errors['reg_first_name_error'] = "First Name can only contain letters"
            is_valid = False
        if not NAME_REGEX.match(request.form['last_name']):
            errors['reg_last_name_error'] = "Last Name can only contain letters"
            is_valid = False
        if len(request.form['email']) < 7:
            errors['reg_email_error'] = 'Email must be at least 7 characters'
            is_valid = False
        if len(request.form['first_name']) < 2:
            errors['reg_first_name_error'] = "First Name MUST be at least 5 characters long"
            is_valid = False
        if len(request.form['last_name']) < 2:
            errors['reg_last_name_error'] = "Last Name MUST be at least 5 characters long"
            is_valid = False
        if not EMAIL_REGEX.match(request.form['email']):
            errors['reg_email_error'] = "Invalid Email Address!"
            is_valid = False
        query1 = "select * from users where users.email = %(email)s;"
        if connectToMySQL(DATABASE).query_db(query1, data=request.form):
            errors['reg_email_error'] = "Email already exists, please Login"
            is_valid = False
        if len(request.form['password']) < 8:
            errors['reg_pw_error'] = "Password must be at least 8 characters"
            is_valid = False
        str1 = request.form['password']
        digits = 0
        uppers = 0
        for i in str1:
            if i.isdigit():
                digits += 1
            if i.isupper():
                uppers += 1
        if digits == 0:
            errors['reg_pw_error'] = 'Password MUST contain at least one number!'
            is_valid = False
        if uppers == 0:
            errors['reg_pw_error'] = 'Password MUST contain at least ONE capital letter!'
            is_valid = False
        if not is_valid:
            msg['status'] = 400
            msg['errors'] = errors
            return jsonify(msg)
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': request.form['password']
        }
        User.registration(data)
        return redirect('/')


@app.route('/register1', methods=['POST'])
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
