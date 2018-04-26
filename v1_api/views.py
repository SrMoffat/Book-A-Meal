"""The application views --> no /api/auth views
"""
from flask import jsonify, make_response, abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.models import Meal, MockDB, Order

from functools import wraps


def clearance_required(access_level):
    """Decorator for restricting access to resources access_level 1 == 'customer' access_level 2 == 'caterer'
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user:
                return make_response(jsonify({"message": "Unauthorized!",
                                              "status": 401}), 401)
            if not current_user.allowed_level(access_level):
                return make_response(jsonify({"message": "Your clearance level is lower than required!",
                                              "status": 401}), 401)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


class Meal(Resource):
    """The Meals resource entity for the API
    """

    @jwt_required
    @clearance_required(2)
    def get_meal(self, meal_id):
        """Gets a single meal querying by id
        """
        meal = MockDB.get_meals(meal_id)
        if not meal:
            return abort(404)
        return meal.meal_holder(), 200

    @jwt_required
    @clearance_required(2)
    def update_meal(self, meal_id):
        """Updates the meal with the meal_id provided
        """
        meal = MockDB.get_meals(meal_id)
        if not meal:
            return abort(404)
        name = request.json.get('name', None)
        price = request.json.get('price', None)
        image_url = request.json.get('image_url', None)

        MockDB.meals.remove(meal)

        if name:
            meal.name = name
        if price:
            meal.price = price
        if image_url:
            meal.image_url = image_url

        MockDB.meals.append(meal)
        return {'id': meal_id,
                'status': '200',
                'message': 'Meal option succesfully updated!'
                }, 200
