release: python manage.py migrate --no-input
web: gunicorn consistently.wsgi
worker: celery worker --app=consistently -l info
