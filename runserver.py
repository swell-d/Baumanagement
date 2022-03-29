#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BM.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    print('http://127.0.0.1:8000/')
    execute_from_command_line([r'C:/Users/WestfaliaBPE/PycharmProjects/BM/manage.py', 'runserver', '0.0.0.0:8000'])


if __name__ == '__main__':
    main()

#  Poedit
#  https://mlocati.github.io/articles/gettext-iconv-windows.html

#  python manage.py makemessages -a -v 3 --ignore venv
#  python manage.py compilemessages --ignore venv
