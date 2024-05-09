from faker import Faker
from faker.providers import date_time
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import db, Farmer, Animal, User, Order, OrderDetail
from datetime import datetime, date
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)
bcrypt = Bcrypt(app)

fake = Faker()
fake.add_provider(date_time)

def clear_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

def create_farmer():
    with app.app_context():
        farmer = Farmer(
            username='farmer',
            email='farmer@example.com',
            farm_name='Farmy Farm',
            location='Farmville'
        )
        farmer.set_password('password')
        db.session.add(farmer)
        db.session.commit()

def seed_animals(num_animals=10):
    with app.app_context():
        for _ in range(num_animals):
            animal = Animal(
                type=fake.word(),
                breed=fake.word(),
                price=fake.random_number(digits=5),
                status=fake.random_element(elements=('Available', 'Sold Out', 'Pending')),
                image_url=fake.image_url()
            )
            db.session.add(animal)
        db.session.commit()

def seed_users(num_users=10):
    with app.app_context():
        for _ in range(num_users):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                address=fake.address()
            )
            user.set_password('password')
            db.session.add(user)
        db.session.commit()

def seed_orders(num_orders=10):
    with app.app_context():
        for _ in range(num_orders):
            order = Order(
                user_id=1,  # Assuming the first user is the farmer
                total_price=fake.random_number(digits=5),
                order_date=fake.date_between(start_date='-5y', end_date='now')
            )
            db.session.add(order)
            db.session.commit()  # Commit order first to get its ID
            
            # Generate order details
            for _ in range(fake.random_int(min=1, max=5)):
                order_detail = OrderDetail(
                    order_id=order.id,
                    animal_id=fake.random_int(min=1, max=10),  # Assuming animal IDs from 1 to 10
                    quantity=fake.random_int(min=1, max=10),
                    unit_price=fake.random_number(digits=5)
                )
                db.session.add(order_detail)
        db.session.commit()

def seed_all():
    clear_data()
    create_farmer()
    seed_animals()
    seed_users()
    seed_orders()

if __name__ == '__main__':
    seed_all()





# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from models import db, Farmer, Animal, User, Order, OrderDetail
# from datetime import datetime, date
# from flask import Flask

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# db.init_app(app)
# bcrypt = Bcrypt(app)

# def clear_data():
#     with app.app_context():
#         db.drop_all()
#         db.create_all()

# def create_farmer():
#     with app.app_context():
#         farmer = Farmer(
#             username='farmer',
#             email='farmer@example.com',
#             farm_name='Farmy Farm',
#             location='Farmville'
#         )
#         farmer.set_password('password')
#         db.session.add(farmer)
#         db.session.commit()

# # Define your real-life animal data here
# REAL_ANIMAL_DATA = [
#     {'type': 'Cow', 'breed': 'Angus', 'price': 500, 'status': 'Available', 'image_url': 'https://example.com/cow.jpg'},
#     {'type': 'Sheep', 'breed': 'Dorper', 'price': 300, 'status': 'Available', 'image_url': 'https://example.com/sheep.jpg'},
#     # Add more animal data as needed
# ]

# def seed_animals():
#     with app.app_context():
#         for animal_data in REAL_ANIMAL_DATA:
#             animal = Animal(**animal_data)
#             db.session.add(animal)
#         db.session.commit()

# # Define your real-life user data here
# REAL_USER_DATA = [
#     {'username': 'john_doe', 'email': 'john@example.com', 'address': '123 Main St, Anytown, USA'},
#     {'username': 'jane_smith', 'email': 'jane@example.com', 'address': '456 Elm St, Othertown, USA'},
#     # Add more user data as needed
# ]

# def seed_users():
#     with app.app_context():
#         for user_data in REAL_USER_DATA:
#             user = User(**user_data)
#             user.set_password('password')
#             db.session.add(user)
#         db.session.commit()

# # Define your real-life order data here
# REAL_ORDER_DATA = [
#     {'user_id': 1, 'total_price': 1500, 'order_date': date(2023, 5, 1)},  # Assuming user ID 1 is the farmer
#     {'user_id': 2, 'total_price': 800, 'order_date': date(2023, 4, 15)},
#     # Add more order data as needed
# ]

# def seed_orders():
#     with app.app_context():
#         for order_data in REAL_ORDER_DATA:
#             order = Order(**order_data)
#             db.session.add(order)
#             db.session.commit()  # Commit order first to get its ID
            
#             # Add real-life order details here if available
#         db.session.commit()

# def seed_all():
#     clear_data()
#     create_farmer()
#     seed_animals()
#     seed_users()
#     seed_orders()

# if __name__ == '__main__':
#     seed_all()
