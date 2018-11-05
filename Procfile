release: python manage.py migrate
web: gunicorn gettingstarted.wsgi --log-file -
clock: python airqo_monitor/clock.py
