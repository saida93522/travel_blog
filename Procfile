release: export DEVELOPMENT=True
release: export USE_S3=FALSE
release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
web: gunicorn travel_blog.wsgi
