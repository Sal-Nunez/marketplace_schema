from flask import Flask
app = Flask(__name__)
app.secret_key = "wubalubadubdub"
app.jinja_env.add_extension('jinja2.ext.do')