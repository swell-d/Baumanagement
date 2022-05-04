from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect

from Baumanagement.models.models_company import CompanyRole, Company
from Baumanagement.models.models_currency import Currency
from Baumanagement.models.models_projects import ProjectLabel, Project
from bank_accounts.models import Account
from bills.models import Bill
from contracts.models import ContractLabel, Contract
from payments.models import Payment


def first_run(request):
    if User.objects.all():
        return redirect('/')

    group = Group.objects.get_or_create(name='admins')[0]

    if request.POST:
        username = request.POST.get('myInputUsername1')
        email = request.POST.get('myInputEmail1')
        password = request.POST.get('myInputPassword1')
        admin = User.objects.create_superuser(username, email, password)
        admin.groups.set([group, ])

        if request.POST.get('myCreateDemoData', '') == 'on':
            create_demo_data(request.LANGUAGE_CODE)

        return redirect('/')

    return render(request, r'registration/first_run.html')


def create_demo_data(lang):
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

    eur = Currency.objects.get_or_create(name='Euro', code='EUR', symbol='€', rate=1)[0]
    usd = Currency.objects.get_or_create(name='US-Dollar', code='USD', symbol='$', rate=1.09)[0]

    role1 = CompanyRole.objects.get_or_create(name=trans['My company'][lang])[0]
    role2 = CompanyRole.objects.get_or_create(name=trans['Supplier'][lang])[0]
    role3 = CompanyRole.objects.get_or_create(name=trans['Client'][lang])[0]

    company1 = Company.objects.get_or_create(name=trans['My company'][lang])[0]
    company1.role.set([role1, ])
    company1.save()

    company2 = Company.objects.get_or_create(name=f"{trans['Supplier'][lang]} #1")[0]
    company2.role.set([role2, ])
    company2.save()

    company3 = Company.objects.get_or_create(name=f"{trans['Client'][lang]} #1")[0]
    company3.role.set([role3, ])
    company3.save()

    company1_account_usd = Account.objects.get_or_create(company=company1, name="USD", currency=usd)[0]
    company3_account_usd = Account.objects.get_or_create(company=company3, name="USD", currency=usd)[0]

    projecttag = ProjectLabel.objects.get_or_create(name=trans['Other'][lang])[0]

    project = Project.objects.get_or_create(name=f"{trans['Project'][lang]} #1", company=company1,
                                            label=projecttag)[0]

    contracttag = ContractLabel.objects.get_or_create(name=trans['Other'][lang])[0]

    contract1 = Contract.objects.get_or_create(name=f"{trans['Contract'][lang]} #1", project=project,
                                               company=company2, type=Contract.BUY, currency=eur,
                                               amount_netto_positiv=100, vat=19, label=contracttag)[0]
    contract2 = Contract.objects.get_or_create(name=f"{trans['Contract'][lang]} #2", project=project,
                                               company=company3, type=Contract.SELL, currency=usd,
                                               amount_netto_positiv=200, vat=19, label=contracttag)[0]

    Bill.objects.get_or_create(name=f"{trans['Bill'][lang]} #1.1", contract=contract1,
                               amount_netto_positiv=50, vat=19)
    Bill.objects.get_or_create(name=f"{trans['Bill'][lang]} #1.2", contract=contract1,
                               amount_netto_positiv=25, vat=19)
    Bill.objects.get_or_create(name=f"{trans['Bill'][lang]} #2.1", contract=contract2,
                               amount_netto_positiv=100, vat=19)
    Bill.objects.get_or_create(name=f"{trans['Bill'][lang]} #2.2", contract=contract2,
                               amount_netto_positiv=50, vat=19)

    Payment.objects.get_or_create(name=f"{trans['Payment'][lang]} #1.1", contract=contract1,
                                  amount_netto_positiv=25, vat=19,
                                  account_from=Account.objects.filter(company=company1).first(),
                                  account_to=Account.objects.filter(company=company2).first())
    Payment.objects.get_or_create(name=f"{trans['Payment'][lang]} #2.1", contract=contract2,
                                  amount_netto_positiv=50, vat=19,
                                  account_from=company3_account_usd,
                                  account_to=company1_account_usd)
