import os

from django.core.management import execute_from_command_line


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'APP.settings')
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    execute_from_command_line(['manage.py', 'test'])
    os.system('python manage.py runserver')


if __name__ == '__main__':
    main()

#  Poedit
#  https://mlocati.github.io/articles/gettext-iconv-windows.html

#  python manage.py makemessages -l de --ignore venv
#  python manage.py compilemessages --ignore venv
