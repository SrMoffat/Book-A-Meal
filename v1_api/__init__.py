"""Book-A-Meal API --> Version 1 (v1)
"""
from flask import Blueprint
from flask_restful import Api, Resource, url_for
from .auth import Register, Login

api_arch = Blueprint('v1_api', __name__)
api = Api(api_arch)

api.add_resource(Register, '/auth/signup')
api.add_resource(Login, '/auth/login')
api.add_resource(Login, '/meals/')
