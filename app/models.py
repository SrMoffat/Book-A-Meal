from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime
from flask import current_app
from flask_jwt_extended import create_access_token
from flask_restful import url_for

STATUS = {
    'cutomer': 1,
    'caterer': 2,
    '4fr0c0d3': 3
}


class User(object):
    """The model for the users in the app
    """
    __CURSOR__ = 1

    def __init__(self, username, email, password, status=STATUS['customer']):
        """The constructor for an instance of a user with default status 'customer'
        """
        self.id = User.__CURSOR__
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.status = status

        User.__CURSOR__ += 1

    def status_caterer(self):
        """Return a user with the status 'caterer'
        """
        return self.status == STATUS['caterer']

    def status_dev(self):
        """Returns a user with status '4fr0c0d3' (super user)
        """
        return self.status == STATUS['4fr0c0d3']

    def clearance(self, clearance_level):
        """Sets a cap for the access priviledge
        """
        return self.role >= clearance_level

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
            'status': self.status
        }
        return user_holder

    
