import os

from django.apps import apps
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

    # Currency = apps.get_model("Baumanagement", "Currency")
    # Currency.objects.get_or_create(name='Euro', code='EUR')
    # Currency.objects.get_or_create(name='US-Dollar', code='USD')
    #
    # Role = apps.get_model("Baumanagement", "Role")
    # Role.objects.get_or_create(name='Meine Firma')

    execute_from_command_line(['manage.py', 'collectstatic'])

    execute_from_command_line(['manage.py', 'test'])


if __name__ == '__main__':
    main()
