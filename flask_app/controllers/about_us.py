from flask_app import app
from flask import render_template

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')