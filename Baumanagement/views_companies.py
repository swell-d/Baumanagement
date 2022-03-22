from django.db.models import QuerySet, Q
from django.shortcuts import render
from django.utils.html import format_html
from django_tables2 import RequestConfig

from Baumanagement.models import Company, CompanyRole, Project, Contract
from Baumanagement.tables import CompanyTable, ProjectTable, ContractTable, PaymentTable, BillTable


def roles_tags():
    filtered_roles = [each for each in CompanyRole.objects.order_by('name') if each.count_companies > 0]
    return format_html(f'<a href="/companies">Alle</a> ({Company.objects.count()}), ' +
                       ', '.join(f'<a href="/companies/{each.id}">{each.name}</a> ({each.count_companies})'
                                 for each in filtered_roles))


def companies(request):
    search = request.GET.get('search')
    if search is not None:
        text_fields = 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number'
        queries = [Q(**{f'{field}__icontains': search}) for field in text_fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        table1 = CompanyTable(Company.objects.filter(qs), order_by="name")
    else:
        table1 = CompanyTable(Company.objects.all(), order_by="name")

    RequestConfig(request).configure(table1)

    context = {'titel1': 'Alle Unternehmen', 'tags1': roles_tags(), 'table1': table1, 'search': search,
               'url': request.path}
    return render(request,
                  'Baumanagement/maintable.html' if search is not None else 'Baumanagement/tables.html',
                  context)


def companies_by_role(request, id):
    table1 = CompanyTable(Company.objects.filter(role=id), order_by="name")
    RequestConfig(request).configure(table1)
    context = {'titel1': f'Unternehmen - {CompanyRole.objects.get(id=id).name}', 'tags1': roles_tags(),
               'table1': table1}
    return render(request, 'Baumanagement/tables.html', context)


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

    return render(request, 'Baumanagement/tables.html', context)
