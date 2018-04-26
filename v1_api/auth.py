from flask_restful import Resource
from flask import request
from app.models import mock_db, User, MockDB


class Register(Resource):
    """The Registration Resource for the API
    """

    def post(self):
        # get post data
        username = request.json['username']
        email = None
        if 'email' in request.json:
            email = request.json['email']
        password = request.json['password']
        clearance = request.json.get('clearance', None)
        if clearance == None:
            clearance = 1
        # create new user
        new_user = User(username, password, email=email, clearance=clearance)

        # buffer double entry
        for person in MockDB.users:
            if username == person.username:
                return {'status': 409,
                        'message': 'Username already exists!'}
        # enforce password requirement
        if not password:
            return {'status': 422,
                    'message': 'Provide password!'
                    }
        # Once validated, create user
        MockDB.users.append(new_user)

        return {'status': 201,
                'message': 'You have been successfully registered!',
                'token': new_user.generate_token()
                }, 201


class Login(Resource):
    """The Login Resource for the API
    """

    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        # enforce username requirement
        if not username:
            return {'status': 400,
                    'message': 'No username provided!'
                    }, 400
        # enforce password requirement
        if not password:
            return {'status': 400,
                    'message': 'No password provided!'
                    }, 400
        # if username and password provided, query for the user
        user = MockDB.return_user(username, password)

        # Raise error if user not in db
        if user == None:
            return {'status': 400,
                    'message': 'Invalid credentials!'
                    }, 400

        # Successful log in
        return {'status': 200,
                'token': user.generate_token()
                }, 200
