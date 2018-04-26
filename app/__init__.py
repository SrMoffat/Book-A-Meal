from flask import Flask
from flask_jwt_extended import JWTManager
from instance.config import app_config
from .models import User, MockDB

from flask_sqlalchemy import SQLAlchemy


jwt = JWTManager()

# enforece token-based authentication with decorator


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    """"Use username to query the db
    """
    user = MockDB.return_user_by_name(identity)
    if user == None:
        return None
    return user


def create_app(config_name):
    """Create and instance of the app with appropriate configurations
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['testing'])
    app.config.from_pyfile('config.py')
    app.config['JWT_SECRET_KEY'] = '4fr0c0d3'

    jwt.init_app(app)
    from v1_api import api_arch as api
    app.register_blueprint(api, url_prefix='/api/v1')

    return app
