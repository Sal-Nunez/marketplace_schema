from flask_app import app
from flask import render_template, redirect, request, session, flash
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
    if not User.validate_login(request.form):
        return redirect('/')
    if not User.check_login(request.form):
        return redirect('/')
    else:
        return redirect('/')

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
