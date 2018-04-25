import os
import unittest
import json
from app import create_app, db


class TestBookMealAPI(unittest.TestCase):
    """
    This class represents the Book-A-Meal application test case
    """

    def setUp(self):
        """
        Method defines text variables and initializes the app with testing configuration
        """
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        # Admin (caterer) authorization token
        self.token = ''
        # Mock data
        self.data = {
            'caterer': {
                "username": "caterer",
                "email": "caterer@mail.com",
                "password": "catererpass",
                "status": "1"
            },
            'customer': {
                "username": "customer",
                "email": "customer@mail.com",
                "password": "customerpass",
                "status": "0"
            },
            'admin': {
                "username": "caterer",
                "password": "catererpass"
            },
            'user': {
                "username": "customer",
                "password": "customerpass"
            },
            'meal': {"id": "1",
                     "name": "chicken mamboleo",
                     "category": "lunch",
                     "price": "$12.00",
                     "image_url": "www.images.com",
                     "description": "2 chicken drumsticks"
                     },
            'new_meal': {"id": "2",
                         "name": "chicken mamboleo",
                         "category": "lunch",
                         "price": "$18.00",
                         "image_url": "www.images.com/1",
                         "description": "2 marinated drumsticks"
                         },
            'daily_menu': {"menu_id": "1",
                           "date_set": "12/12/2022"

                           }
        }
        response = self.client.post("/api/v1/auth/signup", data=json.dumps(self.data['caterer']),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.token = json.loads(response.data)

    def test_root_endpoint(self):
        """Test the root endpoint /api/v1/
        """
        response = self.client.get('/api/v1/')
        self.assertEqual(response.status_code, 200)

    def test_root_view(self):
        """Test the root view of the app "/"
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup_endpoint(self):
        """Test the signup endpoint /api/v1/auth/signup
        """
        response = self.client.post('/api/v1/auth/signup', data=json.dumps(self.data['caterer']),
                                    content_type='application/json')
        # check if content type is in json format
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        # check if response has a token
        response_data = json.loads(response.data)
        self.assertTrue('token' in response_data,
                        msg='No token included in the response')

        # Buffer double registration
        response = self.client.post('/api/v1/auth/signup', data=json.dumps(self.data['caterer']),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_login_endpoint(self):
        """Test the signin endpoint /api/v1/auth/login
        """
        response = self.client.post('/api/v1/auth/login', data=json.dumps(['customer']),
                                    content_type='application/json')
        response = self.client.post('/api/v1/auth/login', data=json.dumps(self.data['admin']),
                                    content_type=application/json)
        # Ensure content-type is json
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # Ensure resonse has token
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response_data)
        self.token = response_data['token']

    def test_create_meal_endpoint(self):
        """Test that the API can create a meal option (POST /api/v1/meals/) accessible by admin only
        """
        # Without Authorization
        response = self.client.post('/api/v1/meals/',
                                    data=json.dumps(self.data['meal']),
                                    content_type='application/json'
                                    )
        # Check authorization
        self.assertEqual(response.status_code, 401)

        # With Authorization
        response = self.client.post('/api/v1/meals/',
                                    data=json.dumps(self.data['meal']),
                                    content_type='application/json',
                                    header=dict(
                                        Authorization='userpass' + self.token)
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('chicken drumsticks', str(response.data))

    def test_get_all_meals(self):
        """Test that the API can get all the meals (GET/api/v1/meals/)
        """
        response = self.client.get('/api/v1/meals/')

        # Check Authorization
        self.assertEqual(response.status_code, 401)
        # With Authorization
        response = self.client.get(
            '/api/v1/meals/', headers=dict(Authorization='userpass' + self.token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.header['Content-Type'], 'application/json')
        response_data = json.loads(response.data)
        self.assertTrue('meals' in response.data)

    def test_get_meal_by_id(self):
        """Test API endpoint can get a meal using meal_id property (GET /api/v1/meals/<int: meal_id>) only for admin
        """
        response = self.client.get(
            '/api/v1/meals/1', data=json.dumps(self.data['meal']))

        # Check Authorization
        self.assertEqual(response.status_code, 401)

        # With Authorization
        response = self.client.get(
            '/api/v1/meals/1', headers=dict(Authorization='userpass' + self.token))
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('chicken', response_data)

    def test_update_meal_endpoint(self):
        """Test API endpoint for updating a meal (PUT/api/v1/meals/<int: meal_id>) accessible only to admin
        """
        response = self.client.put('/api/v1/meals/1', data=json.dumps(self.data['new_meal']),
                                   content_type='application/json')
        # Check Authorization
        self.assertEqual(response.status_code, 401)
        # With Authorization
        response = self.client.put('/api/v1/meals/1', data=json.dumps(self.data['new_meal']),
                                   content_type='application/json',
                                   headers=dict(Authroization='userpass' + self.token))
        self.assertEqual(response.status_code, 200)

    def test_delete_meal_endpoint(self):
        """Test the API endpoint for deleting a meal (DELETE/api/v1/meals/<meal_id>)
        """
        response = self.client.delete('/api/v1/meals/1')
        # Check Authorization
        self.assertEqual(response.status, 401)
        # With Authorization
        response = self.client.delete(
            '/api/v1/meals/1', headers=dict(Authorization='userpass' + self.token))
        self.assertEqual(response.status_code, 204)
        # Check if deleted object still exists
        response = self.client.get(
            '/api/v1/meals/1', headers=dict(Authorization='userpass' + self.token))
        self.assertEqual(response.status_code, 404)

    def test_set_daily_menu_endpoint(self):
        """Test the API endpoint for creating daily menu (POST/api/v1/menu/) only accessible to admin 
        """
        # Check Authorization
        response = self.client.post(
            '/api/v1/menu/', data=json.dumps(self.data['daily_menu']), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        # With Authorization
        response = self.client.post('/api/v1/menu/',
                                    data=json.dumps(self.data['daily_menu']),
                                    content_type='application/json',
                                    headers=dict(Authorization='userpas' + self.token))
        self.assertEqual(response.status_code, 201)

    def test_get_daily_menu_endpoint(self):
        """Test the API endpoint for getting the daily menu (GET/api/v1/menu/) available to authenticated users 
        """
        response = self.client.get('/api/v1/menu/')
        self.assertEqual(response.status_code, 200)

    def test_post_order_endpoint(self):
        """Test the API endpoint for placing an order (POST/order/) available to authenticated users & timebound 
        """
        response = self.client.post('/api/v1/orders/',
                                    data=json.dumps(self.data['selections']),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = {
            "user": 1,
            "meals": [3]
        }
        response = self.client.post('/api/v1/orders/',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_orders_endpoint(self):
        """Test API endpoint for getting all customer orders (GET/api/v1/orders/)
        """
        # Check Authorization
        response = self.client.get('/api/v1/orders/')
        self.assertEqual(response.status_code, 401)
        # With Authorization
        response = self.client.get(
            '/api/v1/orders/', headers=dict(Authorization='userpas' + self.token))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        # delete the --> self.app, --> self.client, and clear self.data and self.token 
        pass
        



if __name__ == '__main__':
    unittest.main()
