release: python manage.py migrate
web: gunicorn gettingstarted.wsgi --log-file -
clock: python gettingstarted/tasks/clock.py
