from django.db.models import QuerySet
from django.forms import ModelForm
from django.utils.html import format_html
from django_tables2 import RequestConfig

from Baumanagement.models import Company, CompanyRole, Project, Contract, add_search_field, Bill, Payment
from Baumanagement.tables import CompanyTable, ProjectTable, ContractTable, PaymentTable, BillTable
from Baumanagement.views import myrender


def roles_tags():
    filtered_roles = [each for each in CompanyRole.objects.order_by('name') if each.count_companies > 0]
    return format_html(f'<a href="/companies">Alle</a> ({Company.objects.count()}), ' +
                       ', '.join(f'<a href="/companies/{each.id}">{each.name}</a> ({each.count_companies})'
                                 for each in filtered_roles))


def companies(request):
    context = {'titel1': 'Alle Unternehmen'}

    if request.method == 'POST':
        formset = CompanyForm(request.POST, request.FILES)
        if formset.is_valid():
            Company(**formset.cleaned_data).save()
    context['form'] = CompanyForm()
    context['buttons'] = ['New']

    queryset = Company.extra_fields(Company.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = CompanyTable(queryset, order_by="name")
    RequestConfig(request).configure(table1)
    context['table1'] = table1
    context['tags1'] = roles_tags()

    return myrender(request, context)


def companies_by_role(request, id):
    role = CompanyRole.objects.get(id=id)
    context = {'titel1': f'Unternehmen - {role.name}'}

    if request.method == 'POST':
        formset = CompanyForm(request.POST, request.FILES)
        if formset.is_valid():
            Company(**formset.cleaned_data).save()
    context['form'] = CompanyForm()
    context['buttons'] = ['New']

    queryset = Company.objects.filter(role=id)
    queryset = Company.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = CompanyTable(queryset, order_by="name")
    RequestConfig(request).configure(table1)
    context['table1'] = table1
    context['tags1'] = roles_tags()

    return myrender(request, context)


def company(request, id):
    company = Company.objects.get(id=id)
    context = {'titel1': f'Unternehmen - {company.name}', 'tables': []}

    if request.method == 'POST':
        formset = CompanyForm(request.POST, request.FILES, instance=company)
        if formset.is_valid():
            company.save()
    context['form'] = CompanyForm(instance=company)
    context['buttons'] = ['Edit']

    queryset = Company.objects.filter(id=id)
    queryset = Company.extra_fields(queryset)
    table1 = CompanyTable(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    projects = Project.objects.filter(company=id)
    projects = Project.extra_fields(projects)
    if projects:
        table = ProjectTable(projects, order_by="name")
        RequestConfig(request).configure(table)
        context['tables'].append({'table': table, 'titel': 'Projekte'})

    contracts = Contract.objects.filter(company=id)
    contracts = Contract.extra_fields(contracts)
    table = ContractTable(contracts, order_by="name")
    RequestConfig(request).configure(table)
    context['tables'].append({'table': table, 'titel': 'Aufträge'})

    if contracts:
        bills = [contract.bills.all() for contract in contracts]
        bills = [Bill.extra_fields(each) for each in bills]
        bills = QuerySet.union(*bills)
        table = BillTable(bills, order_by="id")
        RequestConfig(request).configure(table)
        context['tables'].append({'table': table, 'titel': 'Rechnungen'})

        payments = [contract.payments.all() for contract in contracts]
        payments = [Payment.extra_fields(each) for each in payments]
        payments = QuerySet.union(*payments)
        table = PaymentTable(payments, order_by="id")
        RequestConfig(request).configure(table)
        context['tables'].append({'table': table, 'titel': 'Zahlungen'})

    return myrender(request, context)


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = Company.form_fields()
