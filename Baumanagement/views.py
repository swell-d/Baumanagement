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
    return render(request, 'Baumanagement/1table.html', context)


def role(request, id):
    table = CompanyTable(Company.objects.filter(role=id).all(), order_by="name")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': f'Unternehmen - {CompanyRole.objects.get(id=id).name}',
               'tags': roles_tags()}
    return render(request, 'Baumanagement/1table.html', context)


def projects(request):
    table = ProjectTable(Project.objects.all(), order_by="name")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Projekte'}
    return render(request, 'Baumanagement/1table.html', context)


def contracts(request):
    table = ContractTable(Contract.objects.all(), order_by="id")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Aufträge'}
    return render(request, 'Baumanagement/1table.html', context)


def payments(request):
    table = PaymentTable(Payment.objects.all(), order_by="id")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Zahlungen'}
    return render(request, 'Baumanagement/1table.html', context)


def bills(request):
    table = BillTable(Bill.objects.all(), order_by="id")
    RequestConfig(request).configure(table)
    context = {'table': table,
               'h1': 'Alle Rechnungen'}
    return render(request, 'Baumanagement/1table.html', context)


def test_view(request):
    # data = [', '.join([each2.name for each2 in each.companies.all()]) for each in CompanyRole.objects.all()]
    context = {'data': []}
    return render(request, 'Baumanagement/test.html', context)
