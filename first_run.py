import os

from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BM.settings')

    execute_from_command_line(['manage.py', 'makemigrations', 'Baumanagement'])
    execute_from_command_line(['manage.py', 'migrate'])

    user = get_user_model()
    user.objects.create_superuser('admin', 'admin@myproject.com', 'admin')

    from django.contrib.auth.models import Group
    Group.objects.get_or_create(name='admins')

    execute_from_command_line(['manage.py', 'collectstatic'])

    execute_from_command_line(['manage.py', 'test'])


if __name__ == '__main__':
    main()
