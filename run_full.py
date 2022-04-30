import os

from django.core.management import execute_from_command_line


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BM.settings')
    execute_from_command_line(['manage.py', 'makemigrations', 'Baumanagement'])
    execute_from_command_line(['manage.py', 'migrate'])
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    execute_from_command_line(['manage.py', 'test'])
    print('http://127.0.0.1:8000/')
    os.system('python manage.py runserver 0.0.0.0:8000')


if __name__ == '__main__':
    main()

#  Poedit
#  https://mlocati.github.io/articles/gettext-iconv-windows.html

#  python manage.py makemessages -l en -l de --ignore venv
#  python manage.py compilemessages --ignore venv