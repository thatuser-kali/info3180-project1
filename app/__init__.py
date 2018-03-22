from flask import Flask
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SECRET_KEY'] = "change this to be a more random key"
application.config['UPLOAD_FOLDER'] = 'app/static/profiles'
application.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://project1:password@localhost/profiles"
db = SQLAlchemy(application)
Base = db.Model
session = db.session
