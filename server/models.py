from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String, nullable = False)
    email = db.Column(db.String(100))
    location = db.Column()
    order = db.Column()

class Farmer(db.model):
    __tablename__ = ''