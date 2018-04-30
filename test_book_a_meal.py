import os
import unittest
import json
from app import create_app


class TestBookMealAPI(unittest.TestCase):
    """
    This class represents the Book-A-Meal application test case
    """

    def setUp(self):
        """
        Method defines text variables and initializes the app with testing configuration
        """

        self.app = create_app(config_name='testing')
        self.app = self.app.test_client()

        # Admin (caterer) authorization token
        self.token = ''
        # Mock data
        self.data = {
            'user1': {
                "username": "caterer",
                "email": "caterer@mail.com",
                "password": "catererpass",
                "clearance": 1
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
            'admin_login': {
                "username": "admin",
                "password": "adminpass",
            },
            'add_menu': {
                'meals': [1]
            },
            'order_picked': {
                'meals': [1]
            },
            'order_update': {
                'meals': [2]
            },
            'meal': {
                "id": 1,
                "name": "chicken mamboleo",
                "category": "lunch",
                "price": 40.00,
                "description": "chicken drumsticks "
            },
            'meal_update': {
                "name": "liver lover",
                "price": 50.00,
                "description": "2 chicken drumsticks "
            }
        }
        response = self.app.post("/api/v1/auth/signup",
                                 data=json.dumps(self.data['admin']),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(self.data['admin_login']),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        self.token = json.loads(response.data).get('token', None)

    # def test_root_endpoint(self):
    #     """Test the root endpoint /api/v1/
    #     """
    #     response = self.app.post('/api/v1/')
    #     print(response)
    #     self.assertEqual(response.status_code, 200)

    # def test_root_view(self):
    #     """Test the root view of the app "/"
    #     """
    #     response = self.app.post('/')
    #     self.assertEqual(response.status_code, 200)

    # # POST/api/v1/auth/signup
    def test_signup_endpoint(self):
        """Test the signup endpoint /api/v1/auth/signup
        """
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.data['user1']),
                                 content_type='application/json')
        # check if content type is in json format
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        # check if response has a token
        response_data = json.loads(response.data)
        self.assertTrue('token' in response_data,
                        msg='No token included in the response')

    #     # Buffer double registration
    #     response = self.app.post('/api/v1/auth/signup',
    #                              data=json.dumps(self.data['user1']),
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 409)

    # # POST/api/v1/auth/login
    # def test_login_endpoint(self):
    #     """Test the signin endpoint /api/v1/auth/login
    #     """
    #     response = self.app.post('/api/v1/auth/signup',
    #                              data=json.dumps(['user2']),
    #                              content_type='application/json')
    #     response = self.app.post('/api/v1/auth/login',
    #                              data=json.dumps(self.data['user2_login']),
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     # Ensure content-type is json
    #     self.assertEqual(response.headers['Content-Type'], 'application/json')

    #     # Ensure resonse has token
    #     response_data = json.loads(response.data)
    #     self.assertTrue('token' in response_data)

    # POST/api/v1/meals
    # def test_create_meals_endpoint(self):
    #     """Test the API endpoint for creating a meal (POST/api/v1/meals)
    #     """
    #     response = self.app.post('/api/v1/meals/',
    #                              data=json.dumps(self.data['meal']),
    #                              content_type='application/json',)
    #     # Check authorization
    #     self.assertEqual(response.status_code, 401)

    #     # With authorization
    #     response = self.app.post('/api/v1/meals/',
    #                              data=json.dumps(self.data['meal']),
    #                              content_type='application/json',
    #                              headers=dict(Authorization='Bearer' + self.token))
    #     self.assertEqual(response.status_code, 201)

    #     # GET/api/v1/meal/<meal_id>
    #     def test_get_a_meal_endpoint(self):
    #         """Test the API endpoint for displaying one meal using its meal_id (GET/api/v1/meals/<meal_id>)
    #         """
    #         response = self.app.get('/api/v1/meals',
    #                                 data=json.dumps(self.data['meal']),
    #                                 content_type='application/json',
    #                                 headers=dict(Authorization='Bearer' + self.token))
    #         response_data = json.loads(response.data)
    #         uri = "/api/v1/meal/"+str(res_data.get('id'))
    #         response = self.app.get(uri)

    #         self.assertEqual(response.status_code, 401)
    #         response = self.app.get(uri,
    #                                 content_type='application/json',
    #                                 headers=dict(Authorization='Bearer' + self.token))
    #         self.assertEqual(response.status_code, 200)

    # # PUT/api/v1/meals/<meal_id>
    # def test_update_meal_endpoint(self):
    #     """Test the API endpoint for updating a meal (PUT/api/v1/meals/<meal_id>)
    #     """
    #     response = self.app.post('/api/v1/meals',
    #                              data=json.dumps(self.data['meal']),
    #                              content_type='application/json',
    #                              headers=dict(Authorization='Bearer' + self.token))
    #     self.assertEqual(response.status_code, 201)

    #     response_data = json.loads(response.data)
    #     uri = "/api/v1/meal/"
    #     response = self.app.put(uri+str(response_data['id']),
    #                             data=json.dumps(self.data['meal_update']),
    #                             content_type='application/json')
    #     self.assertEqual(response.status_code, 401)

    #     response = self.app.put(uri+str(response_data['id']),
    #                             data=json.dumps(self.data['meal_update']),
    #                             content_type='application/json',
    #                             headers=dict(Authorization='Bearer' + self.token))
    #     self.assertEqual(response.status_code, 200)
    #     response_data = json.loads(response.data)
    #     response = self.app.get('api/v1/meal/' + str(response_data['id']),
    #                             content_type='application/json',
    #                             headers=dict(Authorization='Bearer' + self.token))
    #     response_data = json.loads(response.data)
    #     self.assertEqual(response_data.get('price'), 50)

    # # DELETE/api/v1/meals/<meal_id>
    # def test_delete_meal_endpoint(self):
    #     """Test the APi endpoint for removing a meal (DELETE/api/v1/meals/<meal_id>)
    #     """
    #     respose = self.app.post('/api/v1/meals',
    #                             data=json.dumps(self.data['meal']),
    #                             content_type="application/json",
    #                             headers=dict(Authorization='Bearer' + self.token))

    #     respose = self.app.delete("/api/v1/meal/1")

    #     self.assertEqual(res.status_code, 401)

    #     respose = self.app.delete("/api/v1/meal/1",
    #                               headers=dict(Authorization='Bearer' + self.token))

    #     self.assertEqual(res.status_code, 200)

    #     respose = self.app.get("/api/v1/meal/1",
    #                            headers=dict(Authorization='Bearer' + self.token))

    #     self.assertEqual(res.status_code, 404)

    # # POST/api/v1/menu
    # def test_create_daily_menu_endpoint(self):
    #     """Test the API endpoint for creating the daily menu (POST/api/v1/menu/) available to admin
    #     """
    #     response = self.app.post('/api/v1/menu/',
    #                              data=json.dumps(self.data['add_menu']),
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 401)
    #     meal = {
    #         'id': 1,
    #         'name': 'chicken mamboleo',
    #         'category': 'lunch',
    #         'price': 12.00,
    #         'description': '2 chicken drumsticks'
    #     }
    #     response = self.app.post('/api/v1/meals/',
    #                              data=json.dumps(meal),
    #                              content_type='application/json',
    #                              headers=dict(Authorization='Bearer' + self.token))
    #     response = self.app.post('/api/v1/menu',
    #                              data=json.dumps(self.data['add_menu']),
    #                              content_type='application/json',
    #                              headers=dict(Authorization='Bearer' + self.token))
    #     self.assertEqual(response.status_code, 201)
    #     self.client.get('/api/v1/menu/')
    #     self.assertEqual(response.status_code, 200)

    # # GET/api/v1/menu
    # def test_get_daily_menu_endpoint(self):
    #     """Test that the API can read and display the daily menu (GET/api/v1/menu/) accessible to admin
    #     """
    #     response = self.app.get('/api/v1/menu')

    #     # Check for authorization (token)
    #     self.assertEqual(response.status_code, 401)

    #     # With authorization
    #     response = self.app.get('/api/v1/menu',
    #                             content_type='application/json',
    #                             headers=dict(Authorization='Bearer' + self.token))
    #     self.assertEqual(response.status_code, 200)

    # # POST/api/v1/orders/
    # def test_place_order_endpoint(self):
    #     """Test that the API can allow users to place orders (POST/api/v1/orders)
    #     """
    #     meal = {
    #         'id': 1,
    #         'name': 'liver lover',
    #         'category': 'lunch',
    #         'price': 15.00,
    #         'description': 'wet fried liver'
    #     }
    #     response = self.app.post('/api/v1/meals',
    #                              data=json.dumps(meal),
    #                              content_type='application/json',
    #                              headers=dict(Authorization='Bearer' + self.token))

    #     response = self.app.post('/api/v1/menu',
    #                              data=json.dumps(self.data['add_menu']),
    #                              content_type='application/json',
    #                              headers=dict(Authorization='Bearer' + self.token))
    #     self.assertEqual(response.status_code, 201)

    #     data = {
    #         "orders": [{
    #             "meal_id": 1,
    #             "quantity": 1
    #         }]
    #     }
    #     response = self.app.post('/api/v1/orders/',
    #                              data=json.dumps(data),
    #                              content_type='application/json',
    #                              headers=dict(Authorization='Bearer' + self.token))
    #     self.assertEqual(response.status_code, 201)

    # # GET/api/v1/orders/
    # def test_get_orders_endpoint(self):
    #     """Test API endpoint for getting all customer orders (GET/api/v1/orders/)
    #     """
    #     # Check Authorization
    #     response = self.app.get('/api/v1/orders/')
    #     self.assertEqual(response.status_code, 401)

    #     # With Authorization
    #     response = self.app.get('/api/v1/orders/',
    #                             headers=dict(Authorization='Bearer' + self.token))
    #     self.assertEqual(response.status_code, 200)

    # # PUT/api/v1/orders/<order_id>
    # def test_update_order_endpoint(self):
    #     """Test that the API updates an order (PUT/api/v1/orders/<order_id>)
    #     """
    #     meal = {
    #         'id': 2,
    #         'name': 'morning glory',
    #         'category': 'breakfast',
    #         'price': 7.00,
    #         'description': 'sausage and bacon'
    #     }
    #     response = self.app.post('/api/v1/meals',
    #                              data=json.dumps(meal),
    #                              content_type='application/json',
    #                              headers=dict(Authorization='Bearer' + self.token))
    #     meal = json.loads(response.data)
    #     meal_id = int(meal['id'])
    #     data = {
    #         'meals': [meal_id]
    #     }
    #     response = self.app.post('/api/v1/menu',
    #                              data=json.dumps(data),
    #                              content_type='application/json',
    #                              headers=dict(Authorization='Bearer' + self.token))

    #     self.assertEqual(response.status_code, 201)

    #     # Mock order
    #     data = {
    #         "orders": [{
    #             "meal_id": meal_id,
    #             "quantity": quantity
    #         }]
    #     }

    #     response = self.app.post('/api/v1/orders',
    #                              data=json.dumps(data),
    #                              content_type='application/json',
    #                              headers=dict(Authorization='Bearer' + self.token))

    #     self.assertEqual(response.status_code, 201)

    #     data = json.loads(response.data)
    #     id = data['orders'][0]['id']
    #     response = self.app.put('/api/v1/order/{}'.format(id),
    #                             data=json.dumps(data),
    #                             content_type='application/json',
    #                             headers=dict(Authorization='Bearer' + self.token))
    #     self.assertEqual(response.status_code, 200)

    def tearDown(self):

        pass


if __name__ == '__main__':
    unittest.main()
