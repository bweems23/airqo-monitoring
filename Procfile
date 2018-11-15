log: tail -f development.log
release: python manage.py migrate
web: gunicorn gettingstarted.wsgi --log-file -
clock: python manage.py run_scheduler
