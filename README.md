# Book-A-Meal
Book-A-Meal is an application that allows users (customers) to make food orders and helps the admins (food vendors) know what the customers want to eat. The front-end is done in HTML 5, CSS 3 and JavaScript powered with a Python-Flask back end. 


# Book-A-Meal UI Templates
You can view my templates here --> https://srmoffat.github.io/Book-A-Meal/UI/index.html
You can view the pages for the UI on the Github Pages site --> https://srmoffat.github.io/Book-A-Meal/UI/index.html
For the dashboard pages navigate to the Github Pages site --> https://srmoffat.github.io/Book-A-Meal/UI/dashboard.html

# UI Installation 
Steps required to interact with the UI elements: 
1. Clone the repository into your local environment:   `git clone https://github.com/SrMoffat/Book-A-Meal` 
2. Switch to book-a-meal directory you just cloned:  `cd Book-A-Meal/UI`
3. Run `index.html` file in your browser. 
4. It will give you these pages:
https://srmoffat.github.io/Book-A-Meal/UI/index.html
https://srmoffat.github.io/Book-A-Meal/UI/dashboard.html

# API Intsallation 
Steps required to interact with the API endpoints:

**Requirements:**

Ensure that you have the following in your machine:
1.Python 3.x
2.Git
3.Browser or Postman 
4.Virutal environment 

Once all requirements are in place:

1. Clone the repo into a folder of your choice: git clone `https://github.com/SrMoffat/Book-A-Meal/`
2. Navigate to the cloned folder `cd Book-A-Meal`
3. Create a virtual environment `virtualenv venv`
4. Activate the virtual environment you just created `cd venv/bin/activate`
5. Install all dependencies into your virtual environment `pip install -r requirements.txt`
6.Confirm you have all packages installed `pip freeze`
7.Set environment variables for APP_SETTINGS `export APP_SETTINGS="development"`
8.Set the entry point for the app `export FLASK_APP="run.py"`

**Run the API**

`flask run` 

**Endpoints on Postman**

1. `POST /api/v1/auth/signup` -->	Creates a user account.
2. `POST /api/v1/auth/login` -->	Logs in a user.
3. `POST /api/v1/meals/`   -->    Add a meal option. Only admin (Caterer) has access.
4. `GET api/v1/meals/`  -->	      Get all meal options. Only admin (Caterer) has access.
5. `PUT api/v1/meals/<mealid>`--> Update the information of a meal option. Only admin (Caterer) has access.
6. `DELETE api/v1/meals/<mealid>`	--> Remove a meal option.Only admin (Caterer) has access.
7. `POST api/v1/menu`  	-->       Set up the menu for the day. Only admin (Caterer) has access.
8. `GET api/v1/menu`  -->	        Get the menu for the day.
9. `POST api/v1/orders`	         Select the meal option from the menu.
10. `PUT api/v1/orders/<orderid>`	Modify an order.
11. `GET api/v1/orders`	Get all the orders.Only admin (Caterer) has access.

**API Documentation**

Find the draft .yaml on swagger documentation here --> https://app.swaggerhub.com/apis/4fr0c0d3/Book-A-Meal/2.0#/


