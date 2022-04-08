import os

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BM.settings')

    execute_from_command_line(['manage.py', 'makemigrations', 'Baumanagement'])
    execute_from_command_line(['manage.py', 'migrate'])

    from django.contrib.auth.models import Group
    group = Group.objects.get_or_create(name='admins')[0]

    user = get_user_model()
    admin = user.objects.filter(username='admin')
    if not admin:
        admin = user.objects.create_superuser('admin', 'admin@myproject.com', 'admin')  # ToDo for pipeline
        admin.groups.set([group, ])

    Currency = apps.get_model("Baumanagement", "Currency")
    eur = Currency.objects.get_or_create(name='Euro', code='EUR', symbol='€', rate=1, created_by=admin)[0]
    usd = Currency.objects.get_or_create(name='US-Dollar', code='USD', symbol='$', rate=1.09, created_by=admin)[0]

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
        'Other': {'en': 'Other', 'de': 'Sonstige'},
    }

    CompanyRole = apps.get_model("Baumanagement", "CompanyRole")
    role1 = CompanyRole.objects.get_or_create(name=trans['My company'][lang], created_by=admin)[0]
    role2 = CompanyRole.objects.get_or_create(name=trans['Supplier'][lang], created_by=admin)[0]
    role3 = CompanyRole.objects.get_or_create(name=trans['Client'][lang], created_by=admin)[0]

    Company = apps.get_model("Baumanagement", "Company")
    company1 = Company.objects.get_or_create(name=trans['My company'][lang], created_by=admin)[0]

    company1.role.set([role1, ])
    company1.save()
    company2 = Company.objects.get_or_create(name=f"{trans['Supplier'][lang]} #1", created_by=admin)[0]
    company2.role.set([role2, ])
    company2.save()
    company3 = Company.objects.get_or_create(name=f"{trans['Client'][lang]} #1", created_by=admin)[0]
    company3.role.set([role3, ])
    company3.save()

    Account = apps.get_model("Baumanagement", "Account")
    company1_account_usd = Account.objects.get_or_create(company=company1, name="USD", currency=usd,
                                                         created_by=admin)[0]
    company3_account_usd = Account.objects.get_or_create(company=company3, name="USD", currency=usd,
                                                         created_by=admin)[0]

    ProjectRole = apps.get_model("Baumanagement", "ProjectRole")
    projectrole = ProjectRole.objects.get_or_create(name=trans['Other'][lang], created_by=admin)[0]

    Project = apps.get_model("Baumanagement", "Project")
    project = Project.objects.get_or_create(name=f"{trans['Project'][lang]} #1", company=company1,
                                            projectrole=projectrole, created_by=admin)[0]

    Contract = apps.get_model("Baumanagement", "Contract")
    contract1 = Contract.objects.get_or_create(name=f"{trans['Contract'][lang]} #1", project=project,
                                               company=company2, type=Contract.BUY, currency=eur,
                                               amount_netto_positiv=100, vat=19, created_by=admin)[0]
    contract2 = Contract.objects.get_or_create(name=f"{trans['Contract'][lang]} #2", project=project,
                                               company=company3, type=Contract.SELL, currency=usd,
                                               amount_netto_positiv=200, vat=19, created_by=admin)[0]

    Bill = apps.get_model("Baumanagement", "Bill")
    Bill.objects.get_or_create(name=f"{trans['Bill'][lang]} #1.1", contract=contract1,
                               amount_netto_positiv=50, vat=19, created_by=admin)
    Bill.objects.get_or_create(name=f"{trans['Bill'][lang]} #1.2", contract=contract1,
                               amount_netto_positiv=25, vat=19, created_by=admin)
    Bill.objects.get_or_create(name=f"{trans['Bill'][lang]} #2.1", contract=contract2,
                               amount_netto_positiv=100, vat=19, created_by=admin)
    Bill.objects.get_or_create(name=f"{trans['Bill'][lang]} #2.2", contract=contract2,
                               amount_netto_positiv=50, vat=19, created_by=admin)

    Payment = apps.get_model("Baumanagement", "Payment")
    Payment.objects.get_or_create(name=f"{trans['Payment'][lang]} #1.1", contract=contract1,
                                  amount_netto_positiv=25, vat=19,
                                  account_from=Account.objects.filter(company=company1).first(),
                                  account_to=Account.objects.filter(company=company2).first(),
                                  created_by=admin)
    Payment.objects.get_or_create(name=f"{trans['Payment'][lang]} #2.1", contract=contract2,
                                  amount_netto_positiv=50, vat=19,
                                  account_from=company3_account_usd,
                                  account_to=company1_account_usd,
                                  created_by=admin)

    execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])


if __name__ == '__main__':
    main()
