from django_tables2 import RequestConfig

from Baumanagement.models import Project, Contract, Payment, Bill, filter_queryset
from Baumanagement.tables import ProjectTable, ContractTable, PaymentTable, BillTable
from Baumanagement.views import myrender


def projects(request):
    queryset = Project.objects.all()
    queryset = filter_queryset(queryset, request)
    table1 = ProjectTable(queryset, order_by="name")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Projekte', 'table1': table1, 'search_field': True}
    return myrender(request, context)


def project(request, id):
    tables = []
    project = Project.objects.get(id=id)

    table1 = ProjectTable(Project.objects.filter(id=id))
    RequestConfig(request).configure(table1)

    contracts = Contract.objects.filter(project=id)
    contracts = Contract.extra_fields(contracts)
    if contracts:
        table = ContractTable(contracts, order_by="name")
        RequestConfig(request).configure(table)
        tables.append({'table': table, 'titel': 'Aufträge'})

    context = {'titel1': f'Projekt - {project.name}', 'table1': table1,
               'tables': tables}
    return myrender(request, context)


def project_payments(request, id):
    project = Project.objects.get(id=id)
    table1 = PaymentTable(Payment.objects.filter(contract__in=project.contracts.all()), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Zahlungen - Projekt - {project.name}', 'table1': table1}
    return myrender(request, context)


def project_bills(request, id):
    project = Project.objects.get(id=id)
    table1 = BillTable(Bill.objects.filter(contract__in=project.contracts.all()), order_by="id")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Rechnungen - Projekt - {project.name}', 'table1': table1}
    return myrender(request, context)
