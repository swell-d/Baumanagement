import os

from django.core.management import execute_from_command_line


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BM.settings')
    execute_from_command_line(['manage.py', 'makemigrations', 'Baumanagement'])
    execute_from_command_line(['manage.py', 'migrate'])
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    execute_from_command_line(['manage.py', 'test'])


if __name__ == '__main__':
    main()
