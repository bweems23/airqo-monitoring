This Repo used Heroku's getting started guide for as a starting point for a simple Django App: https://devcenter.heroku.com/articles/getting-started-with-python

## Running Locally

```sh
$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

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

```sh
$ ./manage.py test airqo_monitor/tests
```

## To enter production python shell

```sh
$ heroku run python manage.py shell
```
