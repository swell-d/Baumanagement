from django.db.models import QuerySet
from django.utils.html import format_html
from django_tables2 import RequestConfig

from Baumanagement.models import Company, CompanyRole, Project, Contract
from Baumanagement.search_fields import companies_search_fields, filter_queryset
from Baumanagement.tables import CompanyTable, ProjectTable, ContractTable, PaymentTable, BillTable
from Baumanagement.views import myrender


def roles_tags():
    filtered_roles = [each for each in CompanyRole.objects.order_by('name') if each.count_companies > 0]
    return format_html(f'<a href="/companies">Alle</a> ({Company.objects.count()}), ' +
                       ', '.join(f'<a href="/companies/{each.id}">{each.name}</a> ({each.count_companies})'
                                 for each in filtered_roles))


def companies(request):
    queryset = Company.objects.all()
    queryset = filter_queryset(queryset, request, companies_search_fields)
    table1 = CompanyTable(queryset, order_by="name")
    RequestConfig(request).configure(table1)
    context = {'titel1': 'Alle Unternehmen', 'tags1': roles_tags(), 'table1': table1, 'search_field': True}
    return myrender(request, context)


def companies_by_role(request, id):
    table1 = CompanyTable(Company.objects.filter(role=id), order_by="name")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Unternehmen - {CompanyRole.objects.get(id=id).name}', 'tags1': roles_tags(),
               'table1': table1}
    return myrender(request, context)


def company(request, id):
    tables = []
    company = Company.objects.get(id=id)

    table1 = CompanyTable(Company.objects.filter(id=id))
    RequestConfig(request).configure(table1)

    projects = Project.objects.filter(company=id)
    if projects:
        table = ProjectTable(projects, order_by="name")
        RequestConfig(request).configure(table)
        tables.append({'table': table, 'titel': 'Projekte'})

    contracts = Contract.objects.filter(company=id)
    if contracts:
        table = ContractTable(contracts, order_by="name")
        RequestConfig(request).configure(table)
        tables.append({'table': table, 'titel': 'Aufträge'})

        bills = QuerySet.union(*[contract.bills.all() for contract in contracts])
        table = BillTable(bills, order_by="id")
        RequestConfig(request).configure(table)
        tables.append({'table': table, 'titel': 'Rechnungen'})

        payments = QuerySet.union(*[contract.payments.all() for contract in contracts])
        table = PaymentTable(payments, order_by="id")
        RequestConfig(request).configure(table)
        tables.append({'table': table, 'titel': 'Zahlungen'})

    context = {'titel1': f'Unternehmen - {company.name}', 'tags1': roles_tags(), 'table1': table1,
               'tables': tables}

    return myrender(request, context)
