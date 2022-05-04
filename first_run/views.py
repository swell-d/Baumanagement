from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from bank_accounts.models import Account
from bills.models import Bill
from companies.models import Company
from companies.models_labels import CompanyLabel
from contracts.models import Contract
from contracts.models_labels import ContractLabel
from currencies.models import Currency
from payments.models import Payment
from products.models import Product
from products.models_labels import ProductCategory
from projects.models import Project
from projects.models_labels import ProjectLabel


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
            create_demo_data()

        return redirect('/')

    return render(request, r'registration/first_run.html')


def create_demo_data():
    eur = Currency.objects.get_or_create(name='Euro', code='EUR', symbol='€', rate=1)[0]
    usd = Currency.objects.get_or_create(name='US-Dollar', code='USD', symbol='$', rate=1.09)[0]

    category = ProductCategory.objects.get_or_create(name=_('Main'))[0]

    base_product = Product.objects.get_or_create(name=_('Base product'), type=Product.PRODUCT,
                                                 amount_netto_positiv=100, vat=19, code='product-1')[0]
    base_product.categories.set([category, ])
    base_product.save()

    base_service = Product.objects.get_or_create(name=_('Base service'), type=Product.SERVICE,
                                                 amount_netto_positiv=50, vat=19, code='service-1')[0]
    base_service.categories.set([category, ])
    base_service.save()

    label1 = CompanyLabel.objects.get_or_create(name=_('My company'))[0]
    label2 = CompanyLabel.objects.get_or_create(name=_('Supplier'))[0]
    label3 = CompanyLabel.objects.get_or_create(name=_('Client'))[0]

    company1 = Company.objects.get_or_create(name=_('My company'))[0]
    company1.label.set([label1, ])
    company1.save()

    company2 = Company.objects.get_or_create(name=_('Supplier') + ' #1')[0]
    company2.label.set([label2, ])
    company2.save()

    company3 = Company.objects.get_or_create(name=_('Client') + ' #1')[0]
    company3.label.set([label3, ])
    company3.save()

    company1_account_usd = Account.objects.get_or_create(company=company1, name="USD", currency=usd)[0]
    company3_account_usd = Account.objects.get_or_create(company=company3, name="USD", currency=usd)[0]

    projecttag = ProjectLabel.objects.get_or_create(name=_('Other'))[0]

    project = Project.objects.get_or_create(name=_('Project') + ' #1', company=company1)[0]
    project.label.set([projecttag, ])
    project.save()

    contracttag = ContractLabel.objects.get_or_create(name=_('Other'))[0]

    contract1 = Contract.objects.get_or_create(name=_('Contract') + ' #1', project=project,
                                               company=company2, type=Contract.BUY, currency=eur,
                                               amount_netto_positiv=100, vat=19)[0]
    contract1.label.set([contracttag, ])
    contract1.save()

    contract2 = Contract.objects.get_or_create(name=_('Contract') + ' #2', project=project,
                                               company=company3, type=Contract.SELL, currency=usd,
                                               amount_netto_positiv=200, vat=19)[0]
    contract2.label.set([contracttag, ])
    contract2.save()

    Bill.objects.get_or_create(name=_('Bill') + ' #1.1', contract=contract1,
                               amount_netto_positiv=50, vat=19)
    Bill.objects.get_or_create(name=_('Bill') + ' #1.2', contract=contract1,
                               amount_netto_positiv=25, vat=19)
    Bill.objects.get_or_create(name=_('Bill') + ' #2.1', contract=contract2,
                               amount_netto_positiv=100, vat=19)
    Bill.objects.get_or_create(name=_('Bill') + ' #2.2', contract=contract2,
                               amount_netto_positiv=50, vat=19)

    Payment.objects.get_or_create(name=_('Payment') + ' #1.1', contract=contract1,
                                  amount_netto_positiv=25, vat=19,
                                  account_from=Account.objects.filter(company=company1).first(),
                                  account_to=Account.objects.filter(company=company2).first())
    Payment.objects.get_or_create(name=_('Payment') + ' #2.1', contract=contract2,
                                  amount_netto_positiv=50, vat=19,
                                  account_from=company3_account_usd,
                                  account_to=company1_account_usd)
