from datetime import datetime, date
from flask import abort, request, jsonify, make_response
from flask_restful import Resource, url_for
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy.sql import extract
from v2_api.mealModel import Meal as MealModel, Menu, Order
from v2_api.userModel import db
from functools import wraps

from v2_api.dbSchema import (
    meals_schema, meal_schema,
    menu_schema, menus_schema,
    orders_schema, order_schema
)


def clearance_required(access_level):
    """Decorator for restricting access to resources access_level 1 == 'customer' access_level 2 == 'caterer'
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user:
                return make_response(jsonify({"message": "Unauthorized!",
                                              "status": 401}), 401)
            if not current_user.access_level(2):
                return make_response(jsonify({"message": "Your clearance level is lower than required!",
                                              "status": 401}), 401)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


class Meal(Resource):
    """The resource item for a meal
    """

    @jwt_required
    @clearance_required(2)
    def get(self, meal_id):
        """GET a meal by id
        """
        meal = MealModel.query.get(meal_id)
        if not meal:
            return abort(404)
        meal_result = meal_schema.dump(meal)
        return meal_result.data, 200

    @jwt_required
    @clearance_required(2)
    def put(self, meal_id):
        """UPDATE a meal by id
        """
        meal = MealModel.query.get(meal_id)
        if not meal:
            return abort(404)
        name = request.json.get('name', None)
        price = request.json.get('price', None)
        description = request.json.get('description', None)
        image_url = request.json.get('image_url', None)

        if name:
            meal.name = name
        if price:
            meal.price = price
        if description:
            meal.description = description
        if image_url:
            meal.image_url = image_url
        meal.save()
        return {
            'status': 200,
            'message': 'Meal has been successfully updated!',
            'id': meal.id,
            'links': {
                'self': url_for('v2_api.mealModel', meal_id=meal.id)
            }
        }, 200

    @jwt_required
    @clearance_required(2)
    def delete(self, meal_id):
        """DELETE a meal by id
        """
        meal = MealModel.query.get(meal_id)
        if not meal:
            return abort(404)
        db.session.delete(meal)
        db.session.comiit()
        return {
            'status': 200,
            'message': 'Meal has been successfully deleted!'
        }, 200


class MealLog(Resource):
    """The resource item for a list of meals
    """
    @jwt_required
    @clearance_required(2)
    def get(self):
        """GET all meals
        """
        meal_log = MealModel.query.all()
        meals = meals_schema.dump(meal_log)
        return {
            'status': 200,
            'meals': meals.data
        }, 200

    @jwt_required
    @clearance_required(2)
    def post(self):
        """CREATE a new meal
        """
        name = request.json.get('name', None)
        category = request.json.get('category', None)
        price = request.json.get('price', None)
        image_url = request.json.get('image_url', None)
        description = request.json.get('description', None)

        meal = MealModel(name=name,
                         category=category,
                         price=price,
                         image_url=image_url,
                         description=description,
                         caterer=current_user)
        meal.save()
        return {
            'status': 201,
            'message': 'Meal has been succesfully created',
            'id': meal.id
        }, 201


class MenuLog(Resource):
    """The reource for the menu items
    """

    @jwt_required
    @clearance_required(1)
    def get(self):
        """GET a menu log with meal items
        """
        menu = Menu.query.filter_by(
            day=date.today()
        ).  filter(Menu.meal != (None)).all()

        menu_response = menus_schema.dump(menu).data
        menu_result = {
            'meals': menu_response,
            'day': str(datetime.today())
        }
        return menu_result, 200

    def post(self):
        """CREATE a menu item
        """
        meals = request.json.get('meals', None)
        menu_elements = []
        for meal_id in meals:
            meal = MealModel.query.get(meal_id)
            if not meal:
                return {
                    'status': 404,
                    'message': 'Meal option cannot be found!',
                    'meal_id': meal_id
                }, 404
            is_menu_item = Menu.query.filter_by(
                day=date.today(),
                meal_id=meal.id).first()
            if is_menu_item:
                return {
                    'status': 409,
                    'message': 'Meal item exists in menu'
                }, 409
            menu_item = Menu(meal_id=meal.id, user_id=current_user.id)
            db.session.add(menu_item)
        db.session.commit()
        return {
            'status': 201,
            'message': 'Menu successfully added!'
        }, 201


class OrderLog(Resource):
    """The resource for the order items
    """
    @jwt_required
    @clearance_required(2)
    def get(self):
        """GET order details
        """
        orders = Order.query.filter_by(delivered=False)
        orders_result = orders_schema.dump(orders).data
        orders_response = {
            'status': 200,
            'orders': orders_result
        }, 200
        return orders_response, 200

    @jwt_required
    @clearance_required(1)
    def post(self):
        """CREATE an order
        """
        request_orders = request.json.get('orders')
        orders = []
        menu = Menu.query.filter_by(
            day=date.today()
        ).all()

        order = Order(user=current_user)
        for order_option in request_orders:
            meal_item = order_option.get('meal_id', None)
            quantity = order_option.get('quantity', None)
            for menu_option in menu:
                if meal_item == menu_option.meal.id:
                    meal = MealModel.query.get(menu_option.meal_id)
                    if not meal:
                        return {
                            'status': 404,
                            'message': 'Meal id {} cannot be located'.format(menu_option.meal_id)
                        }, 404
                    order.meals.append(meal)
                    orders.append(meal)

        if not orders:
            return {
                'status': 201,
                'message': 'Order has been successfully placed!',
                'order': order_schema.dump(order).data
            }, 201


class OrderResource(Resource):
    """The order resource
    """
    @jwt_required
    @clearance_required(1)
    def get(self):
        """GET an order
        """
        order = Order.query.get(order_id)
        return {
            'status': 200,
            'orders': order_schema.dump(order).data
        }, 200

    @jwt_required
    @clearance_required(1)
    def put(self):
        """UPDATE an order
        """
        order = Order.query.get(order_id)
        if not order:
            return abort(404)

        meal_id = request.json.get('meal_id', None)
        menu = Menu.query.filter_by(
            day=date.today(),
            meal_id=meal_id).first()

        if not menu:
            return {
                'status': 404,
                'message': 'Meal option is unavailable!'
            }
        if meal_id:
            order.meal = menu.meal

        order.save()
        return {
            'status': 200,
            'message': 'Order successfully update!',
            'id': order.id
        }, 200
