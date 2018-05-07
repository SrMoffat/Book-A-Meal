"""
--- The Entry Point File for the App ---
            Author: Ngige Gitau 
            For:    Book-A-Meal API 
                    2018       
"""

from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from instance.config import app_config
from .models import User, MockDB
from v2_api.userModel import User
from v2_api.userModel import db


jwt = JWTManager()
ma = Marshmallow()

# enforce token-based authentication with decorator


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    """"Use username to query the db
    """
    user = User.query.filter_by(username=identity).first()
    if user is None:
        return None
    return user


def create_app(config_name):
    """Create and instance of the app with appropriate configurations
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['testing'])
    app.config.from_pyfile('config.py')
    app.config['JWT_SECRET_KEY'] = '4fr0c0d3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    jwt.init_app(app)
    ma.init_app(app)
    from v2_api.api import api2_arch as api
    app.register_blueprint(api, url_prefix='/api/v2')
    db.init_app(app)

    return app
