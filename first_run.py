import os

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BM.settings')

    execute_from_command_line(['manage.py', 'makemigrations', 'Baumanagement'])
    execute_from_command_line(['manage.py', 'migrate'])

    from django.contrib.auth.models import Group
    group = Group.objects.get_or_create(name='admins')

    user = get_user_model()
    admin = user.objects.filter(username='admin')
    if not admin:
        new_user = user.objects.create_superuser('admin', 'admin@myproject.com', 'admin')  # ToDo for pipeline
        new_user.groups.set([group[0], ])

    Currency = apps.get_model("Baumanagement", "Currency")
    Currency.objects.get_or_create(name='Euro', code='EUR')
    Currency.objects.get_or_create(name='US-Dollar', code='USD')

    lang = 'de'  # ToDo for pipeline
    trans = {
        'My company': {'en': 'My company', 'de': 'Meine Firma'},
        'Supplier': {'en': 'Supplier', 'de': 'Anbieter'},
        'Client': {'en': 'Client', 'de': 'Kunde'},
        'Main account': {'en': 'Main account', 'de': 'Haupt Konto'},
        'Buy': {'en': 'Buy', 'de': 'Kauf'},
        'Sale': {'en': 'Sale', 'de': 'Verkauf'},
        'Project': {'en': 'Project', 'de': 'Projekt'},
        'Contract': {'en': 'Contract', 'de': 'Auftrag'},
        'Bill': {'en': 'Bill', 'de': 'Rechnung'},
        'Payment': {'en': 'Payment', 'de': 'Zahlung'},
    }

    CompanyRole = apps.get_model("Baumanagement", "CompanyRole")
    role1 = CompanyRole.objects.get_or_create(name=trans['My company'][lang])
    role2 = CompanyRole.objects.get_or_create(name=trans['Supplier'][lang])
    role3 = CompanyRole.objects.get_or_create(name=trans['Client'][lang])

    Company = apps.get_model("Baumanagement", "Company")
    company1 = Company.objects.get_or_create(name=trans['My company'][lang])

    company1[0].role.set([role1[0], ])
    company1[0].save()
    company2 = Company.objects.get_or_create(name=f"{trans['Supplier'][lang]} #1")
    company2[0].role.set([role2[0], ])
    company2[0].save()
    company3 = Company.objects.get_or_create(name=f"{trans['Client'][lang]} #1")
    company3[0].role.set([role3[0], ])
    company3[0].save()

    Project = apps.get_model("Baumanagement", "Project")
    project = Project.objects.get_or_create(name=f"{trans['Project'][lang]} #1", company=company1[0])

    ContractType = apps.get_model("Baumanagement", "ContractType")
    buy = ContractType.objects.get_or_create(name=trans['Buy'][lang])
    sale = ContractType.objects.get_or_create(name=trans['Sale'][lang])

    Contract = apps.get_model("Baumanagement", "Contract")
    contract1 = Contract.objects.get_or_create(name=f"{trans['Contract'][lang]} #1", project=project[0],
                                               company=company2[0], contract_type=buy[0],
                                               amount_netto=-100, vat=19, amount_brutto=-119)
    contract2 = Contract.objects.get_or_create(name=f"{trans['Contract'][lang]} #2", project=project[0],
                                               company=company3[0], contract_type=sale[0],
                                               amount_netto=200, vat=19, amount_brutto=238)

    Bill = apps.get_model("Baumanagement", "Bill")
    Bill.objects.get_or_create(name=f"{trans['Bill'][lang]} #1.1", contract=contract1[0],
                               amount_netto=-50, vat=19, amount_brutto=-50 * 1.19)
    Bill.objects.get_or_create(name=f"{trans['Bill'][lang]} #1.2", contract=contract1[0],
                               amount_netto=-25, vat=19, amount_brutto=-25 * 1.19)
    Bill.objects.get_or_create(name=f"{trans['Bill'][lang]} #2.1", contract=contract2[0],
                               amount_netto=100, vat=19, amount_brutto=100 * 1.19)
    Bill.objects.get_or_create(name=f"{trans['Bill'][lang]} #2.2", contract=contract2[0],
                               amount_netto=50, vat=19, amount_brutto=50 * 1.19)

    Payment = apps.get_model("Baumanagement", "Payment")
    Payment.objects.get_or_create(name=f"{trans['Payment'][lang]} #1.1", contract=contract1[0],
                                  amount_netto=-25, vat=19, amount_brutto=-25 * 1.19)
    Payment.objects.get_or_create(name=f"{trans['Payment'][lang]} #2.1", contract=contract2[0],
                                  amount_netto=50, vat=19, amount_brutto=50 * 1.19)

    execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])
    execute_from_command_line(['manage.py', 'test'])


if __name__ == '__main__':
    main()
