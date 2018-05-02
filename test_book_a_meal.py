""" Tests for the user authentication """
import unittest
import json
from app import create_app
from app.models import MockDB


class TestBookAMeal(unittest.TestCase):
    """
    This class represents the user authentication test case
    """

    def setUp(self):
        """
        Method create an instance of an app with testing configs then sets data variables
        """

        self.app = create_app(config_name='testing')
        self.app.testing = True
        self.app = self.app.test_client()
        meal = {
            'id': 1,
            'owner': 'owner',
            'name': 'name',
            'category': 'category',
            'price': 1000,
            'image_url': 'url',
            'description': 'desc',
            'date_posted': 'date',
            'order': 0
        }
        MockDB.meals.append(meal)

        self.data = {
            'default': {
                "username": "default",
                "email": "default@mail.com",
                "password": "defaultpass"
            },
            'user1': {
                "username": "caterer",
                "email": "caterer@mail.com",
                "password": "catererpass",
                "clearance": 2
            },
            'user2': {
                "username": "customer",
                "email": "customer@mail.com",
                "password": "customerpass",
                "clearance": 1
            },
            'admin': {
                "username": "admin",
                "email": "admin@mail.com",
                "password": "adminpass",
                "clearance": 2
            },
            'user2_login': {
                "username": "customer",
                "password": "customerpass",
            },
            'null_login': {
                "username": "random",
                "password": "randompass",
            },
            'admin_login': {
                "username": "admin",
                "password": "adminpass",
            },
            'add_menu': {
                'meals': [1]
            }
        }

    # 1. POST/api/v1/auth/signup
    def test_signup_endpoint(self):
        """Test the signup endpoint /api/v1/auth/signup
        """

        uri = "/api/v1/auth/signup"
        response = self.app.post(uri,
                                 data=json.dumps(self.data['default']),
                                 content_type='application/json')
        # Check content-type is json
        self.assertEqual(response.headers['Content-Type'], "application/json")

        # Ensure the response has a token
        response_data = json.loads(response.data)

        self.assertTrue('token' in response_data,
                        msg='No token included in response')

        # Buffer double entry
        response = self.app.post(uri,
                                 data=json.dumps(self.data['default']),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 409)

    # 2. POST/api/v1/auth/login
    def test_login_endpoint(self):
        """Test the signin endpoint /api/v1/auth/login
        """

        uri = "/api/v1/auth/login"

        response = self.app.post("/api/v1/auth/signup",
                                 data=json.dumps(self.data['user2']),
                                 content_type='application/json')

        response = self.app.post(uri,
                                 data=json.dumps(self.data['user2_login']),
                                 content_type='application/json')

        # Check content-type is json
        self.assertEqual(response.headers['Content-Type'], "application/json")

        # Ensure token is included
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response_data,
                        msg='Token not included in response')

    # 3. Test invalid token after user deletion
    def test_invalid_user_token(self):
        """ Test that the token is invalidated after user deletion
        """
        uri = "/api/v1/auth/signup"
        data = {
            "username": "random",
            "email": "random@mail.com",
            "password": "randompass",
            "clearance": 2
        }
        response = self.app.post(uri,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertTrue(response.status_code, 201)

        token = json.loads(response.data).get('token')

        response = self.app.delete(
            '/api/v1/user',
            headers=dict(Authorization='Bearer' + token))

        self.assertTrue(response.status_code, 200)

        response = self.app.get('/api/v1/meals/',
                                content_type='application/json',
                                headers=dict(Authorization='Bearer' + token))

        self.assertTrue(response.status_code, 401)

    # 4. Test password provision
    def test_must_provide_password(self):
        """  Ensure user registration demands for a password 
        """

        uri = "/api/v1/auth/signup"
        data = {
            "username": "maryjane",
            "email": "maryjane@mail.com",
            "clearance": 2
        }
        response = self.app.post(uri,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertTrue(response.status_code, 422)

        uri = "/api/v1/auth/login"
        data = {
            "username": "johndoe"
        }
        response = self.app.post(uri,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertTrue(response.status_code, 400)

        data = {
            "password": "johndoepass"
        }
        response = self.app.post(uri,
                                 data=json.dumps(data),
                                 content_type='application/json')

        self.assertTrue(response.status_code, 400)

    # 5. Test user clearance level
    def test_user_clearance_level(self):
        """ Test the user clearance level
        """
        uri = "/api/v1/auth/signup"
        # Basic user tries level 2 access
        data = {
            "username": "tester",
            "email": "tester@mail.com",
            "password": "testerpassword",
            "clearance": 1
        }
        response = self.app.post(uri,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        token = json.loads(response.data).get('token')
        uri = "/api/v1/meals/"
        meal = {
            "name": "tester meal",
            "category": "breakfast",
            "price": 6.00,
            "image_url": "www.images.com",
            "description": "Tester description here"
        }
        response = self.app.post(uri,
                                 data=json.dumps(meal),
                                 content_type="application/json",
                                 headers=dict(Authorization="Bearer " + token))
        self.assertEqual(response.status_code, 401)

    # 6. POST/api/v1/menu/
    def test_set_day_menu(self):
        """ Test the set day menu endpoint POST/api/v1/menu
        """
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.data['admin']),
                                 content_type='application/json')

        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(self.data['admin_login']),
                                 content_type='application/json')

        token = json.loads(response.data).get('token')

        response = self.app.post('/api/v1/menu/',
                                 data=json.dumps(self.data['add_menu']),
                                 content_type='application/json',
                                 headers=dict(Authorization='Bearer ' + token))

        self.assertEqual(response.status_code, 201)

    def tearDown(self):

        pass


if __name__ == '__main__':
    unittest.main()
