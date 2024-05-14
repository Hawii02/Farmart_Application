# from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session
# from flask_migrate import Migrate
# from models import db, Animal, Farmer, User, Category, Cart, CartItem
# from flask_cors import CORS
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager, create_access_token
# from sqlalchemy.exc import IntegrityError
# import os

# secret_key = os.urandom(16)
# print(secret_key.hex())

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False
# app.config['SECRET_KEY'] = secret_key
# app.config['JWT_SECRET_KEY'] = secret_key
# app.config['SESSION_TYPE'] = 'filesystem'  # Configure session type
# CORS(app)
# bcrypt = Bcrypt(app)
# jwt = JWTManager(app)

# migrate = Migrate(app, db)

# db.init_app(app)
# bcrypt.init_app(app)

# # Farmer Routes
# @app.route('/register/farmer', methods=['POST'])
# def register_farmer():
#     username = request.json['username']
#     email = request.json['email']
#     password = request.json['password']
#     try:
#         new_farmer = Farmer(username=username, email=email)
#         new_farmer.set_password(password)
#         db.session.add(new_farmer)
#         db.session.commit()
#         return jsonify({'message': 'Farmer registered successfully'}), 201
#     except IntegrityError:
#         return jsonify({'message': 'Username or email already exists'}), 400

# @app.route('/login/farmer', methods=['POST'])
# def login_farmer():
#     username = request.json['username']
#     password = request.json['password']
#     farmer = Farmer.query.filter_by(username=username).first()
#     if farmer and farmer.check_password(password):
#         session['farmer_id'] = farmer.id
#         return jsonify({'message': 'Login successful'}), 200
#     return jsonify({'message': 'Invalid credentials'}), 401

# @app.route('/farmer/animals', methods=['POST'])
# def add_animal():
#     if 'farmer_id' not in session:
#         return jsonify({'message': 'Unauthorized'}), 401
#     new_animal = Animal(
#         type=request.json['type'],
#         breed=request.json['breed'],
#         price=request.json['price'],
#         description=request.json['description'],
#         farmer_id=session['farmer_id'],
#         status='Available'  # Default status
#     )
#     db.session.add(new_animal)
#     db.session.commit()
#     return jsonify({'message': 'Animal added successfully'}), 201

# @app.route('/farmer/animals/<int:animal_id>', methods=['PUT'])
# def update_animal(animal_id):
#     if 'farmer_id' not in session:
#         return jsonify({'message': 'Unauthorized'}), 401
#     animal = Animal.query.filter_by(id=animal_id, farmer_id=session['farmer_id']).first()
#     if animal:
#         animal.type = request.json.get('type', animal.type)
#         animal.breed = request.json.get('breed', animal.breed)
#         animal.price = request.json.get('price', animal.price)
#         animal.description = request.json.get('description', animal.description)
#         animal.status = request.json.get('status', animal.status)
#         db.session.commit()
#         return jsonify({'message': 'Animal updated successfully'}), 200
#     return jsonify({'message': 'Animal not found'}), 404

# # User Routes
# @app.route('/register/user', methods=['POST'])
# def register_user():
#     username = request.json['username']
#     email = request.json['email']
#     password = request.json['password']
#     try:
#         new_user = User(username=username, email=email)
#         new_user.set_password(password)
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify({'message': 'User registered successfully'}), 201
#     except IntegrityError:
#         return jsonify({'message': 'Username or email already exists'}), 400

# @app.route('/login/user', methods=['POST'])
# def login_user():
#     username = request.json['username']
#     password = request.json['password']
#     user = User.query.filter_by(username=username).first()
#     if user and user.check_password(password):
#         session['user_id'] = user.id
#         return jsonify({'message': 'Login successful'}), 200
#     return jsonify({'message': 'Invalid credentials'}), 401

# @app.route('/animals', methods=['GET'])
# def list_animals():
#     animals = Animal.query.all()
#     return jsonify([animal.serialize() for animal in animals]), 200

# @app.route('/search/animals', methods=['GET'])
# def search_animals():
#     type_query = request.args.get('type')
#     breed_query = request.args.get('breed')
#     query = Animal.query
#     if type_query:
#         query = query.filter(Animal.type == type_query)
#     if breed_query:
#         query = query.filter(Animal.breed == breed_query)
#     animals = query.all()
#     return jsonify([animal.serialize() for animal in animals]), 200

# # Route to add a new category
# @app.route('/categories', methods=['POST'])
# def add_category():
#     if 'farmer_id' not in session:
#         return jsonify({'message': 'Unauthorized'}), 401
#     category_name = request.json['name']
#     if Category.query.filter_by(name=category_name).first() is not None:
#         return jsonify({'message': 'Category already exists'}), 409
#     new_category = Category(name=category_name)
#     db.session.add(new_category)
#     db.session.commit()
#     return jsonify({'message': 'Category added successfully'}), 201

# # Route to search animals by category
# @app.route('/animals/by_category', methods=['GET'])
# def search_animals_by_category():
#     category_name = request.args.get('category')
#     category = Category.query.filter_by(name=category_name).first()
#     if category is None:
#         return jsonify({'message': 'Category not found'}), 404
#     animals = Animal.query.filter_by(category_id=category.id).all()
#     return jsonify([animal.serialize() for animal in animals]), 200


# @app.route('/cart', methods=['GET'])
# def view_cart():
#     if 'user_id' not in session:
#         return jsonify({'message': 'Unauthorized'}), 401
#     user_id = session['user_id']
#     try:
#         cart = Cart.query.filter_by(user_id=user_id).one()
#         cart_items = [
#             {'animal_id': item.animal_id, 'quantity': item.quantity, 'unit_price': item.animal.price}
#             for item in cart.items
#         ]
#         return jsonify({
#             'total_price': cart.total_price,
#             'status': cart.status,
#             'order_date': cart.order_date,
#             'items': cart_items
#         }), 200
#     except NoResultFound:
#         return jsonify({'message': 'Cart is empty'}), 404

# @app.route('/cart/add', methods=['POST'])
# def add_to_cart():
#     if 'user_id' not in session:
#         return jsonify({'message': 'Unauthorized'}), 401
#     user_id = session['user_id']
#     animal_id = request.json.get('animal_id')
#     quantity = request.json.get('quantity', 1)

#     animal = Animal.query.get_or_404(animal_id, description='Animal not found')
#     cart = Cart.query.filter_by(user_id=user_id).first()

#     if not cart:
#         cart = Cart(user_id=user_id, total_price=0.0, status='Pending')
#         db.session.add(cart)

#     cart_item = CartItem.query.filter_by(cart_id=cart.id, animal_id=animal_id).first()
#     if cart_item:
#         cart_item.quantity += quantity
#     else:
#         cart_item = CartItem(cart_id=cart.id, animal_id=animal_id, quantity=quantity)
#         db.session.add(cart_item)

#     db.session.flush()  # Update the DB state without committing to recalculate total price
#     total_price = sum(item.animal.price * item.quantity for item in cart.items)
#     cart.total_price = total_price
#     db.session.commit()
#     return jsonify({'message': 'Item added to cart', 'total_price': cart.total_price}), 201

# @app.route('/cart/remove/<int:item_id>', methods=['DELETE'])
# def remove_from_cart(item_id):
#     if 'user_id' not in session:
#         return jsonify({'message': 'Unauthorized'}), 401
#     cart_item = CartItem.query.get_or_404(item_id, description='Item not found in your cart')
#     if cart_item.cart.user_id != session['user_id']:
#         return jsonify({'message': 'Operation not allowed'}), 403

#     db.session.delete(cart_item)
#     db.session.flush()  # Update DB state to recalculate total price

#     cart = Cart.query.filter_by(id=cart_item.cart_id).first()
#     cart.total_price = sum(item.animal.price * item.quantity for item in cart.items)
#     db.session.commit()
#     return jsonify({'message': 'Item removed from cart', 'total_price': cart.total_price}), 200

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from models import Animal, Farmer, User, Category, Cart, CartItem
import re
import os

app = Flask(__name__)

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(16).hex()
app.config['JWT_SECRET_KEY'] = os.urandom(16).hex()
CORS(app)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


def validate_email(email):
    valid = re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
    print(f"Validating email '{email}': {'valid' if valid else 'invalid'}")
    return valid

def validate_username(username):
    """Check if the username is at least 3 characters long."""
    return len(username) >= 3

def validate_password(password):
    """Validate password complexity (example: at least 8 characters)."""
    return len(password) >= 8

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    role = data['role'].lower()

    if not validate_email(email) or not validate_username(username) or not validate_password(password):
        return jsonify({'message': 'Validation failed'}), 400

    if role not in ['farmer', 'user']:
        return jsonify({'message': 'Invalid role specified'}), 400

    user_class = Farmer if role == 'farmer' else User
    user = user_class(username=username, email=email, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': f'{role.capitalize()} registered successfully'}), 201
     

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    role = data['role'].lower()

    user_class = Farmer if role == 'farmer' else User
    user = user_class.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity={'id': user.id, 'role': role, 'username': user.username})
        if user.role == role:
            return jsonify(access_token=access_token, id=user.id, username=username, role=role), 200
        else:
            return jsonify({'message': 'Role mismatch'}), 401
    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/farmer/animals', methods=['POST'])
@jwt_required()
def add_animal():
    claims = get_jwt_identity()
    if claims['role'] != 'farmer':
        return jsonify({'message': 'Unauthorized'}), 403
    new_animal = Animal(
        type=request.json['type'],
        breed=request.json['breed'],
        price=request.json['price'],
        description=request.json['description'],
        farmer_id=claims['id'],
        status='Available'
    )
    db.session.add(new_animal)
    db.session.commit()
    return jsonify({'message': 'Animal added successfully'}), 201

@app.route('/farmer/animals/<int:animal_id>', methods=['PUT'])
@jwt_required()
def update_animal(animal_id):
    claims = get_jwt_identity()
    animal = Animal.query.filter_by(id=animal_id, farmer_id=claims['id']).first()
    if animal:
        animal.type = request.json.get('type', animal.type)
        animal.breed = request.json.get('breed', animal.breed)
        animal.price = request.json.get('price', animal.price)
        animal.description = request.json.get('description', animal.description)
        animal.status = request.json.get('status', animal.status)
        db.session.commit()
        return jsonify({'message': 'Animal updated successfully'}), 200
    return jsonify({'message': 'Animal not found'}), 404

@app.route('/animals', methods=['GET'])
def list_animals():
    animals = Animal.query.all()
    return jsonify([animal.serialize() for animal in animals]), 200

@app.route('/animals/by_category', methods=['GET'])
def search_animals_by_category():
    category_name = request.args.get('category')
    category = Category.query.filter_by(name=category_name).first()
    if category:
        animals = Animal.query.filter_by(category_id=category.id).all()
        return jsonify([animal.serialize() for animal in animals]), 200
    return jsonify({'message': 'Category not found'}), 404

@app.route('/categories', methods=['POST'])
@jwt_required()
def add_category():
    claims = get_jwt_identity()
    if claims['role'] != 'farmer':
        return jsonify({'message': 'Unauthorized'}), 403
    category_name = request.json['name']
    if Category.query.filter_by(name=category_name).first():
        return jsonify({'message': 'Category already exists'}), 409
    new_category = Category(name=category_name)
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category added successfully'}), 201

# Error handling
@app.errorhandler(404)
def not_found_error(error):
    print(error)
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    print(error)
    return jsonify({'message': 'An internal error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
