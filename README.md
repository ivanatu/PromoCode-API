
#Promo_Code_Api

In this repo we are basically creating API . We are trying to implement end points for our applicaton to run . The Application will be interacting with the persistent data from the database and this will help us use end points for GET, POST, PUT, DELETE. All the functionalities run with POstman App on the google apps.

About

This is an API for a promo code app that allows safeboda to create , deactivate and view all promo codes

Goal

The goal of this project is to provide a uniform API for safeboda.

Features
Tools

Tools used during the development of this API are;

Flask - this is a python micro-framework
Postgresql - this is a database server

Requirements

Python 2.7.1x+. preferably use Python 3.x.x+
  
Running the application
To run this application on a linux box or windows, execute the following command.
  First create a directory where you want your work to be saved and navigate to that directory
  
    $ open cmd and from that folder git clone https://github.com/ivanatu/PromoCode-API.git
    $ cd PromoCode-API
    $ virtualenv venv
    $ source venv/bin/activate on linux and venv\Scripts\activate on windows
    $ pip install -r requirements.txt
    create 2 postgresql databases for the app and for the tests
    use can name them accordingly i.e promo_code and tests
    $ set SQLALCHEMY_DATABASE_URI=postgresql://postgres:1234@localhost:5432/promo_code
    $ set SQLALCHEMY_DATABASE_URI2=postgresql://postgres:1234@localhost:5432/tests
    $ make sure the TEST variable is turned to False in the init file $ TEST=TRUE
    $ python manage.py db init
    $ python manage.py db migrate
    $ python manage.py db upgrade
    $ python run.py 
    
To run tests,

Tests
   $ cd app    
   $ To run tests,   
   $ make sure the TEST variable is turned to TRUE in the init file
   $ TEST=TRUE  
   $ nosetests app/tests/test_app.py

#### Endpoints for our application
HTTP Method|End point |Action
-----------|----------|--------------|
POST | /generate_code | Creation of a promo code
PUT | /promo_code/<int:id> | Deactivate a particular promo code
GET | /all_promo_codes | Display all promo codes
GET | /active_promo_codes | Display active promo codes
POST | /test_validity | Testing the validity  of a promo code

Note: You can test the end points using postman a google app
For example http://127.0.0.1:5000/all_promo_codes returns all codes in json format

![alt text](https://github.com/ivanatu/PromoCode-API/blob/master/app/static/img/generate%20code%20json%20input.jpg)
![alt text](https://github.com/ivanatu/PromoCode-API/blob/master/app/static/img/deactivate%20promo%20code.jpg)
![alt text](https://github.com/ivanatu/PromoCode-API/blob/master/app/static/img/all%20promo%20codes.jpg)![alt text]
![alt text](https://github.com/ivanatu/PromoCode-API/blob/master/app/static/img/active%20promo%20codes.jpg)
![alt text](https://github.com/ivanatu/PromoCode-API/blob/master/app/static/img/test_validity.jpg)
