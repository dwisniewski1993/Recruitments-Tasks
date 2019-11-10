import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB = 'sqlite:///database.db'
APP = Flask(__name__)
APP.config["SQLALCHEMY_DATABASE_URI"] = DB
APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
DATABASE = SQLAlchemy(APP)
