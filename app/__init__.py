import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
secret_key = os.getenv('SECRET_KEY')
database_uri = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from app import models, routes


with app.app_context():
    db.create_all()
