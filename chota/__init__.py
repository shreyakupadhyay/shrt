from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
#Get the db url from Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
#os.environ['DATABASE_URL']
db = SQLAlchemy(app)


import chota.routes
