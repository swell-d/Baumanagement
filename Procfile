release: python manage.py migrate
release: python manage.py collectstatic --noinput
release: python first_run.py
web: python manage.py runserver 0.0.0.0:\$PORT