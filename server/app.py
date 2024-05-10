from flask import Flask, request,render_template, redirect, url_for, flash, request, jsonify, session
from flask_migrate import Migrate
from models import db, Animal, Farmer, User, Order, OrderDetail , Category
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

@app.before_first_request
def create_tables():
    db.create_all()

# Farmer Routes
@app.route('/register/farmer', methods=['POST'])
def register_farmer():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    try:
        new_farmer = Farmer(username=username, email=email)
        new_farmer.set_password(password)
        db.session.add(new_farmer)
        db.session.commit()
        return jsonify({'message': 'Farmer registered successfully'}), 201
    except IntegrityError:
        return jsonify({'message': 'Username or email already exists'}), 400

@app.route('/login/farmer', methods=['POST'])
def login_farmer():
    username = request.json['username']
    password = request.json['password']
    farmer = Farmer.query.filter_by(username=username).first()
    if farmer and farmer.check_password(password):
        session['farmer_id'] = farmer.id
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/farmer/animals', methods=['POST'])
def add_animal():
    if 'farmer_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    new_animal = Animal(
        type=request.json['type'],
        breed=request.json['breed'],
        price=request.json['price'],
        description=request.json['description'],
        farmer_id=session['farmer_id'],
        status='Available'  # Default status
    )
    db.session.add(new_animal)
    db.session.commit()
    return jsonify({'message': 'Animal added successfully'}), 201

@app.route('/farmer/animals/<int:animal_id>', methods=['PUT'])
def update_animal(animal_id):
    if 'farmer_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    animal = Animal.query.filter_by(id=animal_id, farmer_id=session['farmer_id']).first()
    if animal:
        animal.type = request.json.get('type', animal.type)
        animal.breed = request.json.get('breed', animal.breed)
        animal.price = request.json.get('price', animal.price)
        animal.description = request.json.get('description', animal.description)
        animal.status = request.json.get('status', animal.status)
        db.session.commit()
        return jsonify({'message': 'Animal updated successfully'}), 200
    return jsonify({'message': 'Animal not found'}), 404

# User Routes
@app.route('/register/user', methods=['POST'])
def register_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    try:
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except IntegrityError:
        return jsonify({'message': 'Username or email already exists'}), 400

@app.route('/login/user', methods=['POST'])
def login_user():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/animals', methods=['GET'])
def list_animals():
    animals = Animal.query.all()
    return jsonify([animal.serialize() for animal in animals]), 200

@app.route('/search/animals', methods=['GET'])
def search_animals():
    type_query = request.args.get('type')
    breed_query = request.args.get('breed')
    query = Animal.query
    if type_query:
        query = query.filter(Animal.type == type_query)
    if breed_query:
        query = query.filter(Animal.breed == breed_query)
    animals = query.all()
    return jsonify([animal.serialize() for animal in animals]), 200

# Route to add a new category
@app.route('/categories', methods=['POST'])
def add_category():
    if 'farmer_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    category_name = request.json['name']
    if Category.query.filter_by(name=category_name).first() is not None:
        return jsonify({'message': 'Category already exists'}), 409
    new_category = Category(name=category_name)
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category added successfully'}), 201

# Route to list all categories
@app.route('/categories', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    return jsonify([category.serialize() for category in categories]), 200

# Route to search animals by category
@app.route('/animals/by_category', methods=['GET'])
def search_animals_by_category():
    category_name = request.args.get('category')
    category = Category.query.filter_by(name=category_name).first()
    if category is None:
        return jsonify({'message': 'Category not found'}), 404
    animals = Animal.query.filter_by(category_id=category.id).all()
    return jsonify([animal.serialize() for animal in animals]), 200

# Additional route functionality to list all animals
@app.route('/animals', methods=['GET'])
def list_animals():
    animals = Animal.query.all()
    return jsonify([animal.serialize() for animal in animals]), 200

# @app.route('/cart', methods=['GET'])
# def view_cart():
#     if 'user_id' not in session:
#         return jsonify({'message': 'Unauthorized'}), 401
#     user_id = session['user_id']
#     cart = Cart.query.filter_by(user_id=user_id).first()
#     if not cart:
#         return jsonify({'message': 'Cart is empty'}), 404
#     cart_items = [{'animal_id': item.animal_id, 'quantity': item.quantity} for item in cart.items]
#     return jsonify(cart_items), 200

# @app.route('/cart/add', methods=['POST'])
# def add_to_cart():
#     if 'user_id' not in session:
#         return jsonify({'message': 'Unauthorized'}), 401
#     user_id = session['user_id']
#     animal_id = request.json.get('animal_id')
#     quantity = request.json.get('quantity', 1)  # Default quantity is 1 if not specified

#     # Ensure the animal exists
#     if not Animal.query.get(animal_id):
#         return jsonify({'message': 'Animal not found'}), 404

#     # Retrieve or create a cart
#     cart = Cart.query.filter_by(user_id=user_id).first()
#     if not cart:
#         cart = Cart(user_id=user_id)
#         db.session.add(cart)

#     # Add item to the cart
#     cart_item = CartItem.query.filter_by(cart_id=cart.id, animal_id=animal_id).first()
#     if cart_item:
#         cart_item.quantity += quantity  # Increment the quantity if the item already exists
#     else:
#         new_cart_item = CartItem(cart_id=cart.id, animal_id=animal_id, quantity=quantity)
#         db.session.add(new_cart_item)

#     db.session.commit()
#     return jsonify({'message': 'Item added to cart'}), 201

# @app.route('/cart/remove/<int:item_id>', methods=['DELETE'])
# def remove_from_cart(item_id):
#     if 'user_id' not in session:
#         return jsonify({'message': 'Unauthorized'}), 401
#     cart_item = CartItem.query.get(item_id)
#     if not cart_item or cart_item.cart.user_id != session['user_id']:
#         return jsonify({'message': 'Item not found in your cart'}), 404
#     db.session.delete(cart_item)
#     db.session.commit()
#     return jsonify({'message': 'Item removed from cart'}), 200

if __name__ == '__main__':
    app.run(debug=True)