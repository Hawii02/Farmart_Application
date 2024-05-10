# from faker import Faker
# from faker.providers import date_time
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from models import db, Farmer, Animal, User, Order, OrderDetail
# from datetime import datetime, date
# from flask import Flask

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# db.init_app(app)
# bcrypt = Bcrypt(app)

# fake = Faker()
# fake.add_provider(date_time)

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

# def seed_animals(num_animals=10):
#     with app.app_context():
#         for _ in range(num_animals):
#             animal = Animal(
#                 type=fake.word(),
#                 breed=fake.word(),
#                 price=fake.random_number(digits=5),
#                 status=fake.random_element(elements=('Available', 'Sold Out', 'Pending')),
#                 image_url=fake.image_url()
#             )
#             db.session.add(animal)
#         db.session.commit()

# def seed_users(num_users=10):
#     with app.app_context():
#         for _ in range(num_users):
#             user = User(
#                 username=fake.user_name(),
#                 email=fake.email(),
#                 address=fake.address()
#             )
#             user.set_password('password')
#             db.session.add(user)
#         db.session.commit()

# def seed_orders(num_orders=10):
#     with app.app_context():
#         for _ in range(num_orders):
#             order = Order(
#                 user_id=1,  # Assuming the first user is the farmer
#                 total_price=fake.random_number(digits=5),
#                 order_date=fake.date_between(start_date='-5y', end_date='now')
#             )
#             db.session.add(order)
#             db.session.commit()  # Commit order first to get its ID
            
#             # Generate order details
#             for _ in range(fake.random_int(min=1, max=5)):
#                 order_detail = OrderDetail(
#                     order_id=order.id,
#                     animal_id=fake.random_int(min=1, max=10),  # Assuming animal IDs from 1 to 10
#                     quantity=fake.random_int(min=1, max=10),
#                     unit_price=fake.random_number(digits=5)
#                 )
#                 db.session.add(order_detail)
#         db.session.commit()

# def seed_all():
#     clear_data()
#     create_farmer()
#     seed_animals()
#     seed_users()
#     seed_orders()

# if __name__ == '__main__':
#     seed_all()





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
#     seed_all()# Define your real-life order data here
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



from app import db, app
from models import Animal

def seed_data():
    with app.app_context():

        print('Deleting existing animals...')
        Animal.query.delete()

        print('Creating animals...')

        farmer_id = 1
        category_id = 1

        poultry1 = Animal(type = 'chicken', breed = 'Rhode Island Red', price = 900, status ='Available', description = 'egg laying chicken', image_url = 'https://valleyhatchery.com/wp-content/uploads/2021/11/Rhode-Island-Red-Chicks.webp', farmer_id = farmer_id, category_id = category_id)
        poultry2 = Animal(type = 'turkey', breed = 'Norfolk', price = 2000, status = 'Available', description = 'plump-breasted traditional breed turkey', image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ29k7naaKpvXxIeybQOaQzSFeBVtv5jRUJanCLCJ8kAA&s', farmer_id = farmer_id, category_id = category_id)
        poultry3 = Animal(type = 'geese', breed = 'African', price = 2500, status = 'Available', description = 'meat producers and ornamental birds', image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdYtODTnvUa2JvEJgET9ZLfSgwsYM5hI4qq_BsLwE4Ng&s', farmer_id = farmer_id, category_id = category_id)
        poultry4 = Animal(type = 'duck', breed = 'Pekin', price = 1800, status = 'Available', description = 'snowy white', image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhDEDWh2uwwbnUmc4elpCPlwgl5z6svyaOxw&s', farmer_id = farmer_id, category_id = category_id)

        livestock1 = Animal(type = 'sheep', breed = 'Dorper', price = '7000', status = 'Available', description = 'weighing in at approximately 60 kilograms', image_url = 'https://morningchores.com/wp-content/uploads/2020/12/Dorper-sheep-800x534.jpg', farmer_id = farmer_id, category_id = category_id)
        livestock2 = Animal(type = 'goat', breed = 'Boer', price = '6000', status= 'Available', description = 'white body with a brown head and ears', image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2coiHlSTqgXVzXkNWjfUq1FovlCc5GvKnlReLOfzLWA&s', farmer_id = farmer_id, category_id = category_id)
        livestock3 = Animal(type = 'cow', breed = 'Boran', price = '80000', status = 'Available', description = 'weighs in at 400 kilograms', image_url = 'https://delavidaboran.co.za/images/boran/matings/B05-130%20-%20DIVA%20-%202011.12.29.jpg', farmer_id = farmer_id, category_id = category_id)
        livestock4 = Animal(type = 'sheep', breed = 'Merino', price = '7500', status = 'Available', description = 'adaptable to any weather and has alot of wool', image_url = 'https://sockwellusa.com/cdn/shop/articles/merino-wool-vs-wool-whats-the-difference-379043.jpg?v=1684814363&width=800', farmer_id = farmer_id, category_id = category_id)
        livestock5 = Animal(type = 'goat', breed = 'Saanen', price = '7000', status = 'Available', description = 'heavy milk producers ', image_url = 'https://www.thehappychickencoop.com/wp-content/uploads/2023/02/saanen-goat.jpg', farmer_id = farmer_id, category_id = category_id)

        equines1 =Animal(type = 'horse', breed = 'Arabian', price = 800000, status = 'Available', description = 'matured built brown horse', image_url = 'https://madbarn.com/wp-content/uploads/2023/04/Arabian-Horse-Breen-Profile.jpg', farmer_id = farmer_id, category_id = category_id)
        equines2 = Animal(type = 'horse', breed = 'friesian', price = 1000000, status = 'Available', description = 'stunning black stallion, ten years old', image_url = 'https://cdn.ehorses.media/image/blur/xxldetails/friesian-horses-stallion-7years-16-1-hh-black-dressagehorses-showhorses-breedinghorses-leisurehorses-bad-wurzach_277b9d82-90c9-44cf-9ef4-4ec3633a243e.jpg', farmer_id = farmer_id, category_id = category_id)
        
        camelids1 = Animal(type = 'camel', breed = 'Kharai', price = 70000, status = 'Available', description = 'adapts highly in coastal region', image_url = 'https://www.nativebreed.org/wp-content/uploads/2020/05/Kharai-camel-1024x574.jpg', farmer_id = farmer_id, category_id = category_id)
        camelids2 = Animal(type = 'camel', breed = 'Targui', price = 740000, status = 'Available', description = 'adapts in harsh weather environment', image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRraEqDu1ribiin_YIWD5TVpOECZ6msop1Ja1QZybkj6A&s', farmer_id = farmer_id, category_id = category_id)
        camelids3 = Animal(type = 'camel', breed = 'Dromedary', price = 73000, status = 'Available', description = 'have only one hump', image_url = 'https://i0.wp.com/www.laketobias.com/wp-content/uploads/2021/03/Dromedary-camel-1920x1080-copy.jpg?fit=1920%2C1080&ssl=1', farmer_id = farmer_id, category_id = category_id)
       

        apiary1 = Animal(type = 'bee', breed = 'carpenter', price = 3000, status = 'Available', description = 'body length ranging from about half an inch to over an inch (1.3 to 2.5 centimeters)', image_url = 'https://files.aptuitivcdn.com/Pqnz49oyx5-1775/images/carpenter-bee-identification.jpg', farmer_id = farmer_id, category_id = category_id)
        apiary2 = Animal(type = 'bee',breed = 'honey', price = 4000, status = 'Available', description = 'plays a crucial role in pollination and honey production', image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPTWHCOppZQHniu_mRgwQPyobgj0jWGgNuGlR32x4Glw&s', farmer_id = farmer_id, category_id = category_id)
        apiary3 = Animal(type = 'bee', breed = 'bumble', price = 5100, status = 'Available', description = 'hairy body covered in dense fuzz', image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6rsjpYIrA4_MXqpsc8i2eUqSovmfThiAXOEs0_5Yfow&s', farmer_id = farmer_id, category_id = category_id)

        aquatic1 = Animal(type = 'fish', breed = 'tilapia', price = 1000, status = 'Available', description = 'fast growing fish can grow upto 10 years', image_url = 'https://www.feednavigator.com/var/wrbm_gb_food_pharma/storage/images/_aliases/wrbm_large/publications/feed/feednavigator.com/news/r-d/minty-feed-may-boost-tilapia-survival/9359616-1-eng-GB/Minty-feed-may-boost-tilapia-survival.jpg', farmer_id = farmer_id, category_id = category_id)
        aquatic2 = Animal(type = 'fish', breed = 'mudfish', price = 950, status = 'Available', description = 'covered in thick and scaleless skin', image_url = 'https://t3.ftcdn.net/jpg/00/03/22/66/360_F_3226621_ufBqi6pLrjFl9WXCi5TTVABCDNsPvn.jpg', farmer_id = farmer_id, category_id = category_id)
        aquatic3 = Animal(type = 'fish', breed = 'salmon', price = 5000, status = 'Available', description = 'have silver scales and a silvery-white belly', image_url = 'https://i.ytimg.com/vi/1bUVGUigUIA/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLD2H_n9xkr-262SWroEb4tyMYzPUg', farmer_id = farmer_id, category_id = category_id)
        
        exotic1 = Animal(type = 'ostriches', breed = 'common', price = 120000, status = 'Available', description = 'has a long neck and a large size body', image_url = 'https://www.treehugger.com/thmb/RXeq-0l-3gU8i8f7DBbxUYXYXjI=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/GettyImages-521324136-634374426780412bbd2fdb3bb8c0ba2a.jpg', farmer_id = farmer_id, category_id = category_id)
        exotic2 = Animal(type = 'parrot', breed = 'amazon', price = 30000, status = 'Available', description = 'have a  short square-shaped tails, and vibrant plumage', image_url = 'https://media-be.chewy.com/wp-content/uploads/amazon-parrot.jpg', farmer_id = farmer_id, category_id = category_id)
        
        small_mammals1 = Animal(type = 'rabbit', breed = 'Dutch', price = 4000, status = 'Available', description = 'has white markings on the front of its face', image_url = 'https://homeandroost.co.uk/wp-content/uploads/2021/12/D188EFAF-137B-48AD-8E73-097BB23EC40D-1024x778-1.jpeg', farmer_id = farmer_id, category_id = category_id)
        small_mammals2 = Animal(type = 'rabbit', breed = 'Chinchilla', price = 5000, status = 'Available', description = '10 years old', image_url = 'https://livestockconservancy.org/wp-content/uploads/2022/08/Giant-Chinchilla-Buck-scaled.jpg', farmer_id = farmer_id, category_id = category_id)

        animals =[poultry1, poultry2, poultry3, poultry4, livestock1, livestock2, livestock3, livestock4, livestock5, equines1, equines2, camelids1, camelids2, camelids3, apiary1, apiary2, apiary3, aquatic1, aquatic2, aquatic3, exotic1, exotic2, small_mammals1, small_mammals2]


        db.session.add_all(animals)
        db.session.commit()

        print('Successfully created animals')

if __name__ == '__main__':
    seed_data()






        