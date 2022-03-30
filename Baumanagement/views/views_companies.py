from django.db.models import QuerySet
from django.forms import ModelForm
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Company, CompanyRole, Project, Contract, Bill, Payment
from Baumanagement.tables import CompanyTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table
from Baumanagement.views.views_bills import generate_bills_by_queryset
from Baumanagement.views.views_contracts import generate_contracts_by_queryset
from Baumanagement.views.views_payments import generate_payments_by_queryset
from Baumanagement.views.views_projects import generate_projects_by_queryset

baseClass = Company
tableClass = CompanyTable


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


def objects_table(request):
    context = {'titel1': _('All companies')}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    context['tags1'] = roles_tags()
    return myrender(request, context)


def object_table(request, id):
    queryset = baseClass.objects.filter(id=id)
    context = {'titel1': f'{_("Company")} - {queryset.first().name}', 'tables': []}
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)

    projects = Project.objects.filter(company=id)
    if projects:
        generate_projects_by_queryset(request, context, projects)

    contracts = Contract.objects.filter(company=id)
    generate_contracts_by_queryset(request, context, contracts)

    if contracts:
        bills = [contract.bills.all() for contract in contracts]
        bills = [Bill.extra_fields(each) for each in bills]
        bills = QuerySet.union(*bills)
        generate_bills_by_queryset(request, context, bills)

        payments = [contract.payments.all() for contract in contracts]
        payments = [Payment.extra_fields(each) for each in payments]
        payments = QuerySet.union(*payments)
        generate_payments_by_queryset(request, context, payments)

    return myrender(request, context)


def companies_by_role(request, id):
    role = CompanyRole.objects.get(id=id)
    context = {'titel1': f'{_("Companies")} - {role.name}'}
    queryset = baseClass.objects.filter(role=id)
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    context['tags1'] = roles_tags()
    return myrender(request, context)
