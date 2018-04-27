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
    def get(self, meal_id):
        """Gets a single meal querying by id
        """
        meal = MockDB.get_meals(meal_id)
        if not meal:
            return abort(404)
        return meal.meal_holder(), 200

    @jwt_required
    @clearance_required(2)
    def put(self, meal_id):
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

    @jwt_required
    @clearance_required(2)
    def delete(self, meal_id):
        """Deletes a meal given its meal_id
        """
        meal = MockDB.get_meals(meal_id)
        if not meal:
            return abort(404)
        MockDB.meals.remove(meal)
        return {'status': 200,
                'message': 'Meal option has been succesfully removed!'
                }, 200


class MealLog(Resource):
    """The Meal Item resource entity for the API
    """
    @jwt_required
    @clearance_required(2)
    def get(self):
        """GET the menu item in the API
        """
        meals = {
            'meals': [meal.meal_holder() for meal in MockDB.meals],
            'num_of_meals': len(MockDB.meals),
            'order': 0
        }
        return meals, 200

    def post(self):
        """CREATE meal item in the API
        """
        name = request.json.get('name', None)
        category = request.json.get('category', None)
        price = request.json.get('price', None)
        image_url = request.json.get('image_url', None)
        description = request.json.get('description', None)
        meal = Meal(name, category, price, image_url, description)
        MockDB.meals.append(meal)
        return {'status': 201,
                'id': meal.id,
                'message': 'Meal option succesfully added!'
                }, 201


class MenuLog(Resource):
    """The Menu Item resource in the API
    """
    @jwt_required
    @clearance_required(1)
    def get(self):
        """GET the menu items
        """

        menu_response = {'meals': [meal.meal_holder() for meal in MockDB.menu],
                         'day': None
                         }
        return menu_response, 200

    @jwt_required
    @clearance_required(2)
    def post(self):
        """CREATE the daily menu in the API
        """
        meals = request.json.get('meals', None)
        menu_elements = []

        for meal_id in meals:
            meal = MockDB.get_meals(meal_id)
            if not meal:
                return {'status': 404,
                        'message': 'No meal wwas found!',
                        'meal_id': meal_id
                        }, 404
            menu_elements.append(meal)
            for meal in menu_elements:
                MockDB.menu.append(meal)
        return {'status': 201,
                'message': 'Daily menu succesfully created!',
                'meals': [meal.meal_holder() for meal in menu_elements]
                }, 201


class OrderLog(Resource):
    """The Order Item resource in the API
    """
    @jwt_required
    @clearance_required(2)
    def get(self):
        """GET all orders in the API
        """
        order_response = {
            'orders': [order.order_holder() for order in MockDB.orders]
        }
        return order_response, 200

    @jwt_required
    @clearance_required(1)
    def post(self):
        """CREATE an order in the API
        """
        order_request = request.json.get('orders')
        orders = []

        for order in order_request:
            meal_item = order.get('meal_id')
            quantity = order['quantity']

            for meal in MockDB.menu:
                if meal_item == meal.id:
                    order = Order(meal, current_user, quantity)
                    orders.append(order)

        # Check scope
        if len(orders) != len(order_request):
            return {'status': 404,
                    'message': 'Order not found in menu!'
                    }, 404
        # Add to MockDB
        for order in orders:
            MockDB.orders.append(order)

        return {'status': 201,
                'message': 'Your order has been successully placed!',
                'orders': [order.order_holder() for order in orders]
                }, 201


class OrderResource (Resource):
    """The Order resource for the API
    """
    @jwt_required
    @clearance_required(1)
    def get(self):
        """GET order by id
        """
        order = MockDB.get_order(id)
        return order, 200

    @jwt_required
    @clearance_required(1)
    def put(self):
        """UPADATE order
        """
        order = MockDB.get_order(id)
        if not order:
            return abort(404)

        MockDB.orders.remove(order)

        meal_id = request.json.get('meal_id', None)
        quantity = request.json.get('quantity', None)

        if meal_id:
            meal = MockDB.get_meals(id)
            order.meal = meal
        if quantity:
            order.quantity = quantity

        MockDB.orders.append(order)

        return {'status': 200,
                'message': 'Order has been successfully updated!',
                'id': order.id
                }, 200
