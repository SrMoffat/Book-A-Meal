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

    def test_get_meal_by_id(self):
        """Test API endpoint can get a meal using meal_id property (GET/meal/<int: meal_id>) only for admin
        """
        mock_meal = self.client.post('/meals/', data=self.meal)
        self.assertEqual(mock_meal.status_code, 201)
        result_in_json = json.loads(
            mock_meal.data.decode('utf-8').replace("'", "\""))
        result = self.client.get(
            '/meals/{}'.format(result_in_json['id'])
        )
        self.assertEqual(result.status_code, 200)
        self.assertIn('chicken drumsticks', str(result.data))

    def test_meal_can_be_edited(self):
        """Test Api endpoint can edit an existing meal (PUT/meals/<int: meal_id>) only for admin
        """
        mock_meal = self.client.post(
            '/meals/',
            data={'name': 'morning glory',
                  'category': 'breakfast',
                  'price': '$8.00',
                  'image_url': 'www.images.com/2',
                  'description': 'scotched eggs, french toast, and a sausage'

                  }
        )
        self.assertEqual(mock_meal.status_code, 201)
        mock_meal = self.client.put(
            '/meals/1',
            data={'name': 'changamka',
                  'category': 'breakfast',
                  'price': '$9.00',
                  'image_url': 'www.images.com/2',
                  'description': '2 fried eggs and bacon'

                  }
        )
        self.assertEqual(mock_meal.status_code, 200)
        results = self.client.get('/meals/1')
        self.assertIn('changamka', str(results.data))


if __name__ == '__main__':
    unittest.main()
