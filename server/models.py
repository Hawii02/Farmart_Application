from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt 
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String, nullable = False)
    email = db.Column(db.String(100))
    location = db.Column(db.String)
    order = db.Column(db.Integer)


class Farmer(db.model):
    __tablename__ = 'farmers'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True )
    email = db.Column(db.String(100))
    _password_hash = db.Column(db.String, nullable=False)
    animals = db.Column()
    location = db.Column(db.String)

 
