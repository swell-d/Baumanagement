from django.utils.html import format_html
from django_tables2 import RequestConfig

from Baumanagement.models import Company, CompanyRole, Project, Contract, filter_queryset, Bill, Payment
from Baumanagement.tables import CompanyTable, ProjectTable, ContractTable, PaymentTable, BillTable
from Baumanagement.views import myrender


def roles_tags():
    filtered_roles = [each for each in CompanyRole.objects.order_by('name') if each.count_companies > 0]
    return format_html(f'<a href="/companies">Alle</a> ({Company.objects.count()}), ' +
                       ', '.join(f'<a href="/companies/{each.id}">{each.name}</a> ({each.count_companies})'
                                 for each in filtered_roles))


def companies(request):
    queryset = Company.objects
    queryset = Company.extra_fields(queryset)
    queryset = filter_queryset(queryset, request)
    table1 = CompanyTable(queryset, order_by="name")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Unternehmen', 'tags1': roles_tags(), 'table1': table1, 'search_field': True}
    return myrender(request, context)


def companies_by_role(request, id):
    queryset = Company.objects.filter(role=id)
    queryset = Company.extra_fields(queryset)
    queryset = filter_queryset(queryset, request)
    table1 = CompanyTable(queryset, order_by="name")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Unternehmen - {CompanyRole.objects.get(id=id).name}', 'tags1': roles_tags(),
               'table1': table1, 'search_field': True}
    return myrender(request, context)


def company(request, id):
    tables = []
    company = Company.objects.get(id=id)

    queryset = Company.objects.filter(id=id)
    queryset = Company.extra_fields(queryset)
    table1 = CompanyTable(queryset)
    RequestConfig(request).configure(table1)

    projects = Project.objects.filter(company=id)
    projects = Project.extra_fields(projects)
    if projects:
        table = ProjectTable(projects, order_by="name")
        RequestConfig(request).configure(table)
        tables.append({'table': table, 'titel': 'Projekte'})

    contracts = Contract.objects.filter(company=id)
    contracts = Contract.extra_fields(contracts)
    if contracts:
        table = ContractTable(contracts, order_by="name")
        RequestConfig(request).configure(table)
        tables.append({'table': table, 'titel': 'Aufträge'})

        bills = [contract.bills.all() for contract in contracts]
        bills = Bill.extra_fields(*bills)
        table = BillTable(bills, order_by="id")
        RequestConfig(request).configure(table)
        tables.append({'table': table, 'titel': 'Rechnungen'})

        payments = [contract.payments.all() for contract in contracts]
        payments = Payment.extra_fields(*payments)
        table = PaymentTable(payments, order_by="id")
        RequestConfig(request).configure(table)
        tables.append({'table': table, 'titel': 'Zahlungen'})

    context = {'titel1': f'Unternehmen - {company.name}', 'tags1': roles_tags(), 'table1': table1,
               'tables': tables}

    return myrender(request, context)
