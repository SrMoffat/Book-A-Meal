""" Api Version with Persistence """
from flask import Blueprint, request
from flask_restful import Api, Resource, url_for, abort
from v2_api.api.views import Meal, MealLog, MenuLog
from v2_api.api.auth import Register, Login, UserResource

api2_arch = Blueprint('v2_api', __name__)
api = Api(api2_arch)


@api2_arch.before_request
def assure_json_format():
    """Ensure that the app does not crash in the first instance due to non-json requests
    """
    if request.method == 'POST' and request.method == 'PUT':
        if not request.is_json:
            abort(
                404, message='Application only allows json formatted requests. Add Content-Type header!')


api.add_resource(Register, '/auth/signup')
api.add_resource(Login, '/auth/login')
api.add_resource(Meal, '/meal/<int:meal_id>', endpoint='meal')
api.add_resource(MealLog, '/meals/', endpoint='meals')
api.add_resource(MenuLog, '/menu/')
api.add_resource(UserResource, '/user/')
