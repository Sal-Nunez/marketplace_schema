from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
import datetime

@app.route('/')
def index():
    if not 'uuid' in session:
        return render_template('index.html')
    elif session['uuid'] > 0:
        return redirect('/homepage')

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    if not User.check_login(request.form):
        return redirect('/')
    else:
        return redirect('/homepage')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    else:
        data = {
            'username': request.form['username'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': request.form['password']
        }
        User.registration(data)
    return redirect('/homepage')

@app.route('/homepage')
def homepage():
    if not 'uuid' in session:
        return redirect('/')
    elif session['uuid'] > 0:
        data = {
            'user': User.select(type='id', data={'id': session['uuid']}),
            'users': User.select(),
        }
        return render_template('homepage.html', **data)

@app.route('/logout')
def logout():
    session.pop('uuid')
    return redirect('/homepage')
