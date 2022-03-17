from django.shortcuts import render
from django.utils.html import format_html
from django_tables2 import RequestConfig

from Baumanagement.models import Company, CompanyRole, Project, Contract, Payment, Bill
from Baumanagement.tables import CompanyTable, ProjectTable, ContractTable, PaymentTable, BillTable


def roles_tags():
    filtered_roles = [each for each in CompanyRole.objects.order_by('name') if each.count_companies > 0]
    return format_html(f'<a href="/companies">Alle</a> ({Company.objects.count()}), ' +
                       ', '.join(f'<a href="/companies/{each.id}">{each.name}</a> ({each.count_companies})'
                                 for each in filtered_roles))


def companies(request):
    table = CompanyTable(Company.objects.all(), order_by="name")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Unternehmen',
               'tags': roles_tags()}
    return render(request, 'Baumanagement/tables.html', context)


def company(request, id):
    table = CompanyTable(Company.objects.filter(id=id).all())
    RequestConfig(request).configure(table)

    projects = Project.objects.filter(company=id).all()
    if projects:
        table2 = ProjectTable(projects, order_by="name")
        RequestConfig(request).configure(table2)
        h2 = 'Projekte'
    else:
        table2, h2 = None, None

    contracts = Contract.objects.filter(company=id).all()
    if contracts:
        table3 = ContractTable(contracts, order_by="name")
        RequestConfig(request).configure(table3)
        h3 = 'Aufträge'
    else:
        table3, h3 = None, None

    context = {'table': table,
               'h1': f'Unternehmen - {Company.objects.get(id=id).name}',
               'tags': roles_tags(),
               'table2': table2,
               'h2': h2,
               'table3': table3,
               'h3': h3}
    return render(request, 'Baumanagement/tables.html', context)


def role(request, id):
    table = CompanyTable(Company.objects.filter(role=id).all(), order_by="name")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': f'Unternehmen - {CompanyRole.objects.get(id=id).name}',
               'tags': roles_tags()}
    return render(request, 'Baumanagement/tables.html', context)


def projects(request):
    table = ProjectTable(Project.objects.all(), order_by="name")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Projekte'}
    return render(request, 'Baumanagement/tables.html', context)


def contracts(request):
    table = ContractTable(Contract.objects.all(), order_by="id")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Aufträge'}
    return render(request, 'Baumanagement/tables.html', context)


def payments(request):
    table = PaymentTable(Payment.objects.all(), order_by="id")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Zahlungen'}
    return render(request, 'Baumanagement/tables.html', context)


def bills(request):
    table = BillTable(Bill.objects.all(), order_by="id")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Rechnungen'}
    return render(request, 'Baumanagement/tables.html', context)


def test_view(request):
    # data = [', '.join([each2.name for each2 in each.companies.all()]) for each in CompanyRole.objects.all()]
    context = {'data': []}
    return render(request, 'Baumanagement/test.html', context)
