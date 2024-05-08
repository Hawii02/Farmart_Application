from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from models import db, Animal, Farmer, User, Order, OrderDetail
# from forms import RegistrationForm
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
import os

secret_key = os.urandom(16)
print(secret_key.hex())

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.config['SECRET_KEY'] = secret_key
app.config['JWT_SECRET_KEY'] = secret_key
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


migrate = Migrate(app, db)

db.init_app(app)
bcrypt.init_app(app)