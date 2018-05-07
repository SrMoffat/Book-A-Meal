from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import current_user, jwt_required, create_access_token
from v2_api.userModel import db
from v2_api.userModel import Clearance, User
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
            if not current_user.access_level(2):
                return make_response(jsonify({"message": "Your clearance level is lower than required!",
                                              "status": 401}), 401)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


class Register(Resource):
    """User registration resource for API
    """

    def post(self):
        """CREATE a new user
        """
        username = request.get_json().get('username', None)
        email = None
        if 'email' in request.get_json():
            email = request.get_json().get('email')
        password = request.get_json().get('password', None)

        if not password:
            return {
                'status': 422,
                'message': 'Invalid password'
            }, 422

        clearance = request.get_json().get('clearance', None)
        if clearance is None:
            clearance = 1

        permission = Clearance.query.filter_by(
            clearance_level=clearance).first()

        check_user_exists = User.query.filter_by(username=username).first()
        if check_user_exists:
            return {
                'status': 409,
                'message': 'The user already exists!'
            }, 409

        user = User(username=username, password=password,
                    clearance=permission, email=email)
        input_is_valid, errs = user.data_validation()
        if not input_is_valid:
            return {
                'errors': errs
            }, 400

        user.save()
        return {
            'status': 201,
            'message': 'User successfully registered',
            'token': user.make_token()
        }, 201


class Login(Resource):
    """User login resource for the API
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str,
                                 location='json', required=True)
        self.parser.add_argument('password', type=str,
                                 location='json', required=True)

    def post(self):
        args = self.parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        user = User.query.filter_by(username=username).first()

        if user is None:
            return {
                'status': 400,
                'message': 'User does not exist!'
            }, 400
        if not user.verify_password(password):
            return {
                'status': 400,
                'message': 'Invalid password!'
            }, 400

        return {
            'status': 200,
            'token': user.make_token()
        }, 200


class UserResource(Resource):
    """User handler resource
    """
    @jwt_required
    @clearance_required(2)
    def delete(self):
        """Remove a user
        """
        db.session.delete(current_user)
        db.session.commit()
        return {
            'status': 200,
            'message': 'User has been successfully removed!'
        }
