This Repo used Heroku's getting started guide as a starting point for a simple Django App: https://devcenter.heroku.com/articles/getting-started-with-python

## Running Locally

clone the repo and...

install requirements:
```sh
$ pip install -r requirements.txt
```

create basic test data:
```sh
$  python manage.py create_test_data
```

run the server:
```sh
$ python manage.py runserver
```

Your app should now be running on [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Deploying to Heroku

Install Jeroku CLI https://devcenter.heroku.com/articles/heroku-cli

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)

## Running Tests

To run all tests in the whole app:
```sh
$ ./manage.py test --pattern="test_*.py"
```
If you add a new test folder, you'll need to add an empty `__init__.py` file in order for the above command to pick it up.

To run tests from one folder:
```sh
$ ./manage.py test airqo_monitor/tests
```

## To enter production python shell

```sh
$ heroku run python manage.py shell
```
