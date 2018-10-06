# Fast Food Fast API

[![Build Status](https://travis-ci.org/ThaDeveloper/FastFoodFast_API.svg?branch=challenge2)](https://travis-ci.org/ThaDeveloper/FastFoodFast_API)
[![Coverage Status](https://coveralls.io/repos/github/ThaDeveloper/FastFoodFast_API/badge.svg?branch=challenge2)](https://coveralls.io/github/ThaDeveloper/FastFoodFast_API?branch=challenge2)
[![Maintainability](https://api.codeclimate.com/v1/badges/3fd60e594cbe166cb1c9/maintainability)](https://codeclimate.com/github/ThaDeveloper/FastFoodFast_API/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d6469fbb16a1418e99213fc9ea862c3b)](https://www.codacy.com/app/ThaDeveloper/FastFoodFast_API?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ThaDeveloper/FastFoodFast_API&amp;utm_campaign=Badge_Grade)

A Restful API to power the Fast-Food-Fast delivery app.

## Getting Started

To have this code on your local machine for running and testing, simply run:
` $ git clone https://github.com/ThaDeveloper/FastFoodFast_API`

### Prerequisites

You need to have the following installed in your local machine:
- [Python3](https://www.python.org/download/releases/3.0/)
- [Pip3](https://pypi.org/project/pip/) - On linux run `sudo apt-get install python3-pip`
- [virtual environment](http://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv) - on your terminal run `pip install virtualenv` 

### Installing

#### Version 1
To install and run version 1 of FastFoodFast_API simply:
`$ cd FastFoodFast_API`
1. Create and activate virtual env
- `virtualenv  -p python3 venv`
- `$ source venv/bin/activate`
2. `$ pip install -r requirements.txt` to install the dependencies
3. Setup environment varibles. You need the following in your .env file:
- export FLASK_APP=run.py
- export FLASK_ENV=development
- export SECRET='yoursecret'
Activate the env variables by `$source .env`
4. Using - run `$ python3 run.py`
Launch [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en) and access the following endpoints:

Order
1. `POST: http://127.0.0.1:5000/api/v1/orders` - Post an order - user
2. `GET: http://127.0.0.1:5000/api/v1/orders/order_id `- Get a specific order - user or admin
3. `GET: http://127.0.0.1:5000/api/v1/orders` - Get all orders - admin
4. `PUT: http://127.0.0.1:5000/api/v1/orders/order_id` - Update order status - admin
5. `PUT: http://127.0.0.1:5000/api/v1/orders/order_id/edit` - Edit an order by user
6. `DELETE: http://127.0.0.1:5000/api/v1/orders/order_id` - Delete an order by user
7. `GET: http://127.0.0.1:5000/api/v1/orders/customer` - View user order history
 
Menu
1. `GET http://127.0.0.1:5000/api/v1/menu` - View full menu
2. `GET http://127.0.0.1:5000/api/v1/menu/<int:id>` - Get single menu item
3. `POST http://127.0.0.1:5000/api/v1/menu` - Add menu item
4. `PUT http://127.0.0.1:5000/api/v1/menu/<int:id>` - Update menu item
5. `PUT http://127.0.0.1:5000/api/v1/menu/<int:id>` - Delete menu item

User
1. `POST: /api/v1/auth/register`- User registration
2. `POST: /api/v1/auth/login` - User login

Or can simply test the hosted version by replacing `http://127.0.0.1:5000` with `https://fastfoodfast-api.herokuapp.com`

*Sample input data*

```
Sample user register data:
{
"first_name": "Kunta",
"last_name": "Kinte",
"username": "kunta.kinte",
"email": "kuntatest@gmail.com",
"password": "#123pass"
}

Sample order data:

{
"items": {"burger": 2, "pizza": 3}
}
Available pre-added menu items to test:

{
    'burger': {
        'item_id': 1,
        'name': 'burger',
        'image': 'burger.jpg',
        'price': 800,
        'category': 'snacks'},
    'pizza': {
        'item_id': 2,
        'name': 'pizza',
        'image': 'pizza.jpg',
        'price': 1000,
        'category': 'snacks'}
}
Available admin to test:
{
    'admin': {'id': 1,
        'first_name': 'Super',
        'last_name': 'User',
        'username': 'admin',
        'email': 'super.user@fastfood.com',
        'password': 'password',
        'admin': True
    }
}
```
#### Version 2
To install and run version 2 of FastFoodFast_API simply:
`$ cd FastFoodFast_API`
1. Create and activate virtual env
- `virtualenv  -p python3 venv`
- `$ source venv/bin/activate`
2. `$ pip install -r requirements.txt` to install the dependencies
3. Setup environment varibles. Copy all from .env_sampe and paste them into the .env file. Update the values to your choice.
Activate the env variables by `$source .env`. For testing set `FLASK_ENV` to `testing` and if development set it to `development`.
4. Run migrations: `$ python3 manage.py create_db`
4. Using - run `$ python3 run.py` or `$flask run`
Launch [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en) and access the following endpoints:

Order
1. `POST: http://127.0.0.1:5000/api/v2/auth/user/orders` - Post an order - user
2. `GET: http://127.0.0.1:5000/api/v2/orders/order_id `- Get a specific order - admin
3. `GET: http://127.0.0.1:5000/api/v2/orders` - Get all orders - admin
4. `PUT: http://127.0.0.1:5000/api/v2/orders/order_id` - Update order status - admin
5. `PUT: http://127.0.0.1:5000/api/v2/auth/users/orders/order_id` - Edit an order by user
6. `DELETE: http://127.0.0.1:5000/api/v2/auth/users/orders/order_id` - Delete an order by user
7. `GET: http://127.0.0.1:5000/api/v2/auth/users/orders` - View user order history
 
Menu
1. `GET http://127.0.0.1:5000/api/v2/menu` - View full menu
2. `GET http://127.0.0.1:5000/api/v2/menu/<int:id>` - Get single menu item
3. `POST http://127.0.0.1:5000/api/v2/menu` - Add menu item
4. `PUT http://127.0.0.1:5000/api/v2/menu/<int:id>` - Update menu item
5. `PUT http://127.0.0.1:5000/api/v2/menu/<int:id>` - Delete menu item

User
1. `POST: /api/v2/auth/register`- User registration
2. `POST: /api/v2/auth/login` - User login
3. `DELETE: /api/v2/auth/logout` - User logout
4. `GET: /api/v2/auth/users` - View all users - superuser only endpoint
5. `POST: /api/v2/auth/users/id/promote` - Promote normal user to admin - superuser only endpoint.The superuser is auto created so use the password you set on .env and `superuser` username to login.

Or can simply test the hosted version by replacing `http://127.0.0.1:5000` with `https://fastfoodfast-api.herokuapp.com`

##### Documentation
Check out the full documentation of the FastFoodFast API on [Swagger Docs](https://app.swaggerhub.com/apis/justin.ndwiga/FastFoodFast/1.0.0)
## Running tests
1. Check all passes - `$ pytest`
2. Check coverage - `$nosetests --with-coverage --cover-package=app`

## Deployment 
Live on [heroku](https://fastfoodfast-api.herokuapp.com/)

## Built With
- [Flask](http://flask.pocoo.org/)

## Authors
[Justin Ndwiga](https://github.com/ThaDeveloper)

## License
MIT License

Copyright (c) 2018 Justin Ndwiga

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

```THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.```
