from django.db.models import QuerySet
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
    table1 = CompanyTable(Company.objects.all(), order_by="name")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Unternehmen', 'tags1': roles_tags(), 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


def company(request, id):
    table1, table2, table3, table4, table5 = None, None, None, None, None

    table1 = CompanyTable(Company.objects.filter(id=id))
    RequestConfig(request).configure(table1)

    projects = Project.objects.filter(company=id)
    if projects:
        table2 = ProjectTable(projects, order_by="name")
        RequestConfig(request).configure(table2)

    contracts = Contract.objects.filter(company=id)
    if contracts:
        table3 = ContractTable(contracts, order_by="name")
        RequestConfig(request).configure(table3)

        bills = QuerySet.union(*[contract.bills.all() for contract in contracts])
        table4 = BillTable(bills, order_by="id")
        RequestConfig(request).configure(table4)

        payments = QuerySet.union(*[contract.payments.all() for contract in contracts])
        table5 = PaymentTable(payments, order_by="id")
        RequestConfig(request).configure(table5)

    context = {'titel1': f'Unternehmen - {Company.objects.get(id=id).name}', 'tags1': roles_tags(), 'table1': table1,
               'titel2': 'Projekte', 'table2': table2,
               'titel3': 'Aufträge', 'table3': table3,
               'titel4': 'Rechnungen', 'table4': table4,
               'titel5': 'Zahlungen', 'table5': table5}
    return render(request, 'Baumanagement/tables.html', context)


def role(request, id):
    table1 = CompanyTable(Company.objects.filter(role=id), order_by="name")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Unternehmen - {CompanyRole.objects.get(id=id).name}', 'tags1': roles_tags(),
               'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


def projects(request):
    table1 = ProjectTable(Project.objects.all(), order_by="name")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Projekte', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


def project(request, id):
    table1 = ProjectTable(Project.objects.filter(id=id))
    RequestConfig(request).configure(table1)

    contracts = Contract.objects.filter(project=id)
    if contracts:
        table2 = ContractTable(contracts, order_by="name")
        RequestConfig(request).configure(table2)
        titel2 = 'Aufträge'
    else:
        table2, titel2 = None, None

    context = {'titel1': f'Projekt - {Project.objects.get(id=id).name}', 'table1': table1,
               'titel2': titel2, 'table2': table2}
    return render(request, 'Baumanagement/tables.html', context)


def contracts(request):
    table1 = ContractTable(Contract.objects.all(), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Aufträge', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


def payments(request):
    table1 = PaymentTable(Payment.objects.all(), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Zahlungen', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


def project_payments(request, id):
    project = Project.objects.get(id=id)
    table1 = PaymentTable(Payment.objects.filter(contract__in=project.contracts.all()), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Zahlungen - Projekt - {project.name}', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


def bills(request):
    table1 = BillTable(Bill.objects.all(), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Rechnungen', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


def test_view(request):
    context = {'data': []}
    return render(request, 'Baumanagement/test.html', context)
