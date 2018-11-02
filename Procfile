release: python manage.py migrate
web: gunicorn gettingstarted.wsgi --log-file -
clock: python python manage.py runjobs hourly
