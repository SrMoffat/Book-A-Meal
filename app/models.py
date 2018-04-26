from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime
from flask import current_app
from flask_jwt_extended import create_access_token
from flask_restful import url_for

CLEARANCE = {
    'guest': 0,
    'customer': 1,
    'caterer': 2,
    '4fr0c0d3': 3
}


class User(object):
    """The model for the users in the app
    """
    __CURSOR = 1

    def __init__(self, username, password, email=None, clearance=CLEARANCE['customer']):
        """The constructor for an instance of a user with default clearance 'customer'
        """
        self.id = User.__CURSOR
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.clearance = clearance

        User.__CURSOR += 1

    def clearance_caterer(self):
        """Return a user with the clearance 'caterer'
        """
        return self.clearance == CLEARANCE['caterer']

    def clearance_dev(self):
        """Returns a user with clearance '4fr0c0d3' (super user)
        """
        return self.clearance == CLEARANCE['4fr0c0d3']

    def access_level(self, clearance_level):
        """Sets a cap for the access priviledge
        """
        return self.clearance >= clearance_level

    def verify_passwords(self, password):
        """Confirm that the passwords' hash values match
        """
        return check_password_hash(self.password_hash, password)

    def generate_token(self):
        """Generate the access token for the users
        """
        return create_access_token(identity=self.username)

    def user_info(self):
        """Holder for the user and their information
        """
        user_holder = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'clearance': self.clearance
        }
        return user_holder


class Meal(object):
    """The model for the meals in the app
    """
    __CURSOR = 1

    def __init__(self, name, category, price, image_url, description, caterer: User):
        """Constructor for the meal with attributes and owner 'caterer'
        """
        self.id = Meal.__CURSOR
        self.name = name
        self. category = category
        self.price = int(price)
        self.image_url = image_url
        self.description = description
        self.caterer = caterer
        self.date_posted = datetime.utcnow()

        Meal.__CURSOR += 1

    def meal_holder(self):
        """Return the meal in form of a dict
        """
        return {
            'id': self.id,
            'owner': self.caterer.id,
            'meal': {
                'name': self.name,
                'category': self.category,
                'price': self.price,
                'image_url': self.image_url,
                'description': self.description,
                'date_posted': str(self.date_posted)
            },
            'order': 0
        }


class Order(object):
    """The model for the orders in the application
    """
    __CURSOR = 1

    def __init__(self, meal: Meal, user: User, quantity=1):
        """Construcor for the order with attributes and quantity default set to 1
        """
        self.id = Order.__CURSOR
        self.meal = meal
        self.owner = user
        self.quantity = quantity
        self.time_ordered = datetime.utcnow()

        Order.__CURSOR += 1

    def get_order_owner(self):
        """Get the owner of an order
        """
        return self.owner

    def increment_order_quantity(self, quantity=1):
        """To change the order quantity incrementally by one 
        """
        self.quantity += quantity

    def order_holder(self):
        """The holder for the order details
        """
        return {
            'id': self.id,
            'owner': self.user.user_info(),
            'quantity': self.quantity,
            'time_placed': str(self.time_ordered)
        }


mock_db = {
    'users': [],  # User table
    'meals': [],  # Meals table
    'orders': [],  # Orders table
}


class MockDB(object):
    """The model to querry the mock_db and its table
    """
    users = []
    orders = []
    meals = []
    menu = []

    @classmethod
    def return_user(cls, username, password):
        """Class method to query and return a user
        """
        for user in cls.users:
            if user.username == username and user.verify_passwords(password):
                return user

    @classmethod
    def return_user_by_name(cls, username):
        """Class method to query users by name
        """
        for user in cls.users:
            if username == user.username:
                return user

    @classmethod
    def get_meals(cls, id):
        """Class method to query for meals
        """
        for meal in cls.meals:
            if meal.id == id:
                return meal
