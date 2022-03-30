from django.contrib import messages
from django.db.models import QuerySet
from django.forms import ModelForm
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from Baumanagement.models.abstract import add_search_field
from Baumanagement.models.models import Company, CompanyRole, Project, Contract, Bill, Payment
from Baumanagement.tables import CompanyTable, ProjectTable, ContractTable, PaymentTable, BillTable
from Baumanagement.views.views import myrender, upload_files


def roles_tags():
    html = f'''<a href="{reverse('companies')}">{_('All')}</a> ({Company.objects.count()}), '''
    html += ', '.join(
        f'''<a href="{reverse('companies_id', args=[role.id])}">{role.name}</a> ({role.count_companies})'''
        for role in CompanyRole.objects.order_by('name') if role.count_companies > 0)
    return format_html(html)


def companies(request):
    context = {'titel1': _('All companies')}
    form_new_company(request, context)

    queryset = Company.extra_fields(Company.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = CompanyTable(queryset, order_by="name", orderable=request.GET.get('search') is None)
    RequestConfig(request).configure(table1)
    context['table1'] = table1
    context['tags1'] = roles_tags()

    return myrender(request, context)


def companies_by_role(request, id):
    role = CompanyRole.objects.get(id=id)
    context = {'titel1': f'{_("Companies")} - {role.name}'}
    form_new_company(request, context)

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
    context = {'titel1': f'{_("Company")} - {company.name}', 'tables': []}
    form_edit_company(request, context, company)

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


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = Company.form_fields


def form_new_company(request, context):
    if request.method == 'POST':
        formset = CompanyForm(request.POST, request.FILES)
        if formset.is_valid():
            new_object = Company(**formset.cleaned_data)
            new_object.save()
            messages.success(request, f'{new_object.name} {_("created")}')
            upload_files(request, new_object)
    context['form'] = CompanyForm()
    context['files_form'] = []
    context['buttons'] = ['New']


def form_edit_company(request, context, company):
    if request.method == 'POST':
        formset = CompanyForm(request.POST, request.FILES, instance=company)
        if formset.is_valid():
            company.save()
            messages.success(request, f'{company.name} {_("changed")}')
            upload_files(request, company)
    context['form'] = CompanyForm(instance=company)
    context['files_form'] = company.files
    context['buttons'] = ['Edit']
