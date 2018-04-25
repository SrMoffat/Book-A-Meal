import unittest
import os
import json
from app import create_app, db


class TestBookMeal(unittest.TestCase):
    """
    This class represents the Book-A-Meal test case
    """

    def setUp(self):
        """
        Method defines text variables and initializes the app
        """
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.meal = {'name': 'chicken mamboleo',
                     'category': 'lunch',
                     'price': '$12.00',
                     'image_url': 'www.images.com',
                     'description': '2 chicken drumsticks'
                     }
        # with self.app.app_context():
        #     db.create_all()

    def test_meal_creation(self):
        """Test that the API can create a meal option (POST/meals/) accessible by admin only
        """
        response = self.client.post('/meals/', data=self.meal)
        self.assertEqual(response.status_code, 201)
        self.assertIn('chicken drumsticks', str(response.data))

    def test_get_all_meals(self):
        """Test that the API can get all the created meal options (GET/meals/) accessible by admin only
        """
        response = self.client.post('/meals/', data=self.meal)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/meals/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('chicken drumsticks', str(response.data))


if __name__ == '__main__':
    unittest.main()
