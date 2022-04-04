import os

from django.apps import apps
from django.core.management import execute_from_command_line
from django.utils.translation import gettext_lazy as _


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BM.settings')

    execute_from_command_line(['manage.py', 'makemigrations', 'Baumanagement'])
    execute_from_command_line(['manage.py', 'migrate'])

    # ContractType = apps.get_model("Baumanagement", "ContractType")
    # ContractType.objects.get_or_create(name=_('Buy'))
    # ContractType.objects.get_or_create(name=_('Sell'))


if __name__ == '__main__':
    main()
