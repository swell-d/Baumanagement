from django.db.models import Q
from django.shortcuts import render
from django_tables2 import RequestConfig

from Baumanagement.models import Project, Contract, Payment, Bill
from Baumanagement.tables import ProjectTable, ContractTable, PaymentTable, BillTable


def projects(request):
    search = request.GET.get('search')
    if search is not None:
        text_fields = 'name', 'code', 'company__name', 'address', 'city', 'land'
        queries = [Q(**{f'{field}__icontains': search}) for field in text_fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        table1 = ProjectTable(Project.objects.filter(qs), order_by="name")
    else:
        table1 = ProjectTable(Project.objects.all(), order_by="name")

    RequestConfig(request).configure(table1)

    context = {'titel1': 'Alle Projekte', 'table1': table1, 'search': search, 'url': request.path}
    return render(request,
                  'Baumanagement/maintable.html' if search is not None else 'Baumanagement/tables.html',
                  context)


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
