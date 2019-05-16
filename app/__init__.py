import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize application
promoapp = Flask(__name__, static_folder=None)
TEST = False

promoapp.config['DEBUG'] = True
if os.environ.get('DATABASE_URL'):
    promoapp.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    if TEST:
        promoapp.config['SQLALCHEMY_DATABASE_URI2'] = os.environ['SQLALCHEMY_DATABASE_URI2']
    else:
        promoapp.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']

promoapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
promoapp.config['SECRET_KEY'] = os.environ['SECRET_KEY']
db = SQLAlchemy(promoapp)
db.init_app(promoapp)

from . import views

