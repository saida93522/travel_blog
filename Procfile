release: export DEVELOPMENT=True
release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
web: gunicorn travel_blog.wsgi
