# Book-A-Meal
Book-A-Meal is an application that allows users (customers) to make food orders and helps the admins (food vendors) know what the customers want to eat. The front-end is done in HTML 5, CSS 3 and JavaScript powered with a Python-Flask back end. 


# Book-A-Meal UI Templates
You can view my templates here --> https://srmoffat.github.io/Book-A-Meal/UI/index.html
You can view the pages for the UI on the Github Pages site --> https://srmoffat.github.io/Book-A-Meal/UI/index.html
For the dashboard pages navigate to the Github Pages site --> https://srmoffat.github.io/Book-A-Meal/UI/dashboard.html

# UI Installation 
Steps required to interact with the UI elements: 
Clone the repository into your local environment:   `git clone https://github.com/SrMoffat/Book-A-Meal` 
Switch to book-a-meal directory you just cloned:  `cd Book-A-Meal/UI`
Run `index.html` file in your browser. 
It will give you these pages:
https://srmoffat.github.io/Book-A-Meal/UI/index.html
https://srmoffat.github.io/Book-A-Meal/UI/dashboard.html

# API Intsallation 
Steps required to interact with the API endpoints:

**Requirements: **

Ensure that you have the following in your machine:
1. Python 3.x
2. Git
3. Browser or Postman 
4. Virutal environment 

Once all requirements are in place:

Clone the repo into a folder of your choice: git clone `https://github.com/SrMoffat/Book-A-Meal/`
Navigate to the cloned folder `cd Book-A-Meal`
Create a virtual environment `virtualenv venv`
Activate the virtual environment you just created `source venv/bin/activate`
Install all dependencies into your virtual environment `pip install -r requirements.txt`
Confirm you have all packages installed `pip freeze`
Set environment variables for APP_SETTINGS `export APP_SETTINGS="development"`
Set the entry point for the app `export FLASK_APP="run.py"`

**Run the API**

`flask run` 

**Endpoints on Postman**

`POST /api/v1/auth/signup` -->	Creates a user account.
`POST /api/v1/auth/login` -->	Logs in a user.
`POST /api/v1/meals/` -->	Add a meal option. Only admin (Caterer) has access.
`GET api/v1/meals/` -->	Get all meal options. Only admin (Caterer) has access.
`PUT api/v1/meals/<mealid>`	--> Update the information of a meal option. Only admin (Caterer) has access.
`DELETE api/v1/meals/<mealid>`	--> Remove a meal option.Only admin (Caterer) has access.
`POST api/v1/menu`	--> Set up the menu for the day. Only admin (Caterer) has access.
`GET api/v1/menu` -->	Get the menu for the day.
`POST api/v1/orders`	Select the meal option from the menu.
`PUT api/v1/orders/<orderid>`	Modify an order.
`GET api/v1/orders`	Get all the orders.Only admin (Caterer) has access.

**API Documentation**

Find the document on -->


