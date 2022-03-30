from django.db.models import QuerySet
from django.forms import ModelForm
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from Baumanagement.models.abstract import add_search_field
from Baumanagement.models.models import Company, CompanyRole, Project, Contract, Bill, Payment
from Baumanagement.tables import CompanyTable, ProjectTable, ContractTable, PaymentTable, BillTable
from Baumanagement.views.views import myrender, new_object_form, edit_object_form

baseClass = Company


class FormClass(ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def roles_tags():
    html = f'''<a href="{reverse('companies')}">{_('All')}</a> ({baseClass.objects.count()}), '''
    html += ', '.join(
        f'''<a href="{reverse('companies_id', args=[role.id])}">{role.name}</a> ({role.count_companies})'''
        for role in CompanyRole.objects.order_by('name') if role.count_companies > 0)
    return format_html(html)


def companies(request):
    context = {'titel1': _('All companies')}
    new_object_form(request, context, FormClass)

    queryset = baseClass.extra_fields(baseClass.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = CompanyTable(queryset, order_by="name", orderable=request.GET.get('search') is None)
    RequestConfig(request).configure(table1)
    context['table1'] = table1
    context['tags1'] = roles_tags()

    return myrender(request, context)


def companies_by_role(request, id):
    role = CompanyRole.objects.get(id=id)
    context = {'titel1': f'{_("Companies")} - {role.name}'}
    new_object_form(request, context, FormClass)

    queryset = baseClass.objects.filter(role=id)
    queryset = baseClass.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = CompanyTable(queryset, order_by="name")
    RequestConfig(request).configure(table1)
    context['table1'] = table1
    context['tags1'] = roles_tags()

    return myrender(request, context)


def company(request, id):
    company = baseClass.objects.get(id=id)
    context = {'titel1': f'{_("Company")} - {company.name}', 'tables': []}
    edit_object_form(request, context, FormClass, company)

    queryset = baseClass.objects.filter(id=id)
    queryset = baseClass.extra_fields(queryset)
    table1 = CompanyTable(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    projects = Project.objects.filter(company=id)
    projects = Project.extra_fields(projects)
    if projects:
        table = ProjectTable(projects, order_by="name")
        RequestConfig(request).configure(table)
        context['tables'].append({'table': table, 'titel': _("Projects")})

    contracts = Contract.objects.filter(company=id)
    contracts = Contract.extra_fields(contracts)
    table = ContractTable(contracts, order_by="name")
    RequestConfig(request).configure(table)
    context['tables'].append({'table': table, 'titel': _("Contracts")})

    if contracts:
        bills = [contract.bills.all() for contract in contracts]
        bills = [Bill.extra_fields(each) for each in bills]
        bills = QuerySet.union(*bills)
        table = BillTable(bills, order_by="id")
        RequestConfig(request).configure(table)
        context['tables'].append({'table': table, 'titel': _("Bills")})

        payments = [contract.payments.all() for contract in contracts]
        payments = [Payment.extra_fields(each) for each in payments]
        payments = QuerySet.union(*payments)
        table = PaymentTable(payments, order_by="id")
        RequestConfig(request).configure(table)
        context['tables'].append({'table': table, 'titel': _("Payments")})

    return myrender(request, context)
