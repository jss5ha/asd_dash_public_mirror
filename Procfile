release: python manage.py migrate
web: gunicorn -- chdir directory/ dash.wsgi --log-level debug
