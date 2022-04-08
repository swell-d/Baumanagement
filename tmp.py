import os

from django.apps import apps
from django.core.management import execute_from_command_line
from django.utils.translation import gettext_lazy as _


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BM.settings')

    execute_from_command_line(['manage.py', 'makemigrations', 'Baumanagement'])
    execute_from_command_line(['manage.py', 'migrate'])

    # ContractTag = apps.get_model("Baumanagement", "ContractTag")
    # ContractTag.objects.get_or_create(name=_('Buy'))
    # ContractTag.objects.get_or_create(name=_('Sell'))


if __name__ == '__main__':
    main()
