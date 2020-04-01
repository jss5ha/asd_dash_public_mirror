release: python manage.py migrate
python manage.py collectstatic --noinput
web: gunicorn -- dash.wsgi --log-level debug
