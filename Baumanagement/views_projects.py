from django.shortcuts import render
from django_tables2 import RequestConfig

from Baumanagement.filters import ProjectFilter, filter_form_prettify
from Baumanagement.models import Project, Contract, Payment, Bill
from Baumanagement.tables import ProjectTable, ContractTable, PaymentTable, BillTable


def projects(request):
    filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    table1 = ProjectTable(filter.qs, order_by="name")
    RequestConfig(request).configure(table1)
    filter_form = filter_form_prettify(filter.form)

    context = {'titel1': 'Alle Projekte', 'table1': table1,
               'filter': filter, 'filter_form': filter_form}
    return render(request, 'Baumanagement/tables.html', context)


def project(request, id):
    tables = []
    project = Project.objects.get(id=id)

    table1 = ProjectTable(Project.objects.filter(id=id))
    RequestConfig(request).configure(table1)

    contracts = Contract.objects.filter(project=id)
    if contracts:
        table = ContractTable(contracts, order_by="name")
        RequestConfig(request).configure(table)
        tables.append({'table': table, 'titel': 'Aufträge'})

    context = {'titel1': f'Projekt - {project.name}', 'table1': table1,
               'tables': tables}
    return render(request, 'Baumanagement/tables.html', context)


def project_payments(request, id):
    project = Project.objects.get(id=id)
    table1 = PaymentTable(Payment.objects.filter(contract__in=project.contracts.all()), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Zahlungen - Projekt - {project.name}', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


def project_bills(request, id):
    project = Project.objects.get(id=id)
    table1 = BillTable(Bill.objects.filter(contract__in=project.contracts.all()), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Rechnungen - Projekt - {project.name}', 'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)
