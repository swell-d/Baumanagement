import json
import os

import requests
from django.apps import apps
from django.core.management import execute_from_command_line


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'APP.settings')
    execute_from_command_line(['manage.py', 'migrate'])

    Currency = apps.get_model("Baumanagement", "Currency")
    symbols = [each.code for each in Currency.objects.all()]
    symbols.remove('EUR')
    symbols = ','.join(symbols)
    with open('apikeys.json', 'r') as file:
        dct = json.loads(file.read())
    request = requests.get(f'http://data.fixer.io/api/latest?access_key={dct["fixer"]}&base=EUR&symbols={symbols}')
    response = request.json()

    for each in Currency.objects.all():
        if each.code == 'EUR':
            continue
        each.rate = response['rates'][each.code]
        each.save()


if __name__ == '__main__':
    main()
