from django.forms import ModelForm
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Bill, Payment
from Baumanagement.models.models_company import CompanyRole, Company
from Baumanagement.tables.tables_companies import CompanyTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table
from Baumanagement.views.views_accounts import generate_accounts_by_queryset
from Baumanagement.views.views_bills import generate_bills_by_queryset
from Baumanagement.views.views_contacts import generate_contacts_by_queryset
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
    context = {}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    context['tags1'] = roles_tags()
    return myrender(request, context)


def object_table(request, id):
    context = {'tables': []}
    queryset = baseClass.objects.filter(id=id)
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)

    accounts = queryset.first().accounts.all()
    generate_accounts_by_queryset(request, context, accounts)

    contacts = queryset.first().contacts.all()
    generate_contacts_by_queryset(request, context, contacts)

    projects = queryset.first().projects.all()
    generate_projects_by_queryset(request, context, projects)

    contracts = queryset.first().contracts.all()
    generate_contracts_by_queryset(request, context, contracts)

    bills = Bill.objects.filter(contract__company=queryset.first())
    generate_bills_by_queryset(request, context, bills)

    payments = Payment.objects.filter(contract__company=queryset.first())
    generate_payments_by_queryset(request, context, payments)

    return myrender(request, context)


def companies_by_role(request, id):
    role = CompanyRole.objects.get(id=id)
    context = {'titel1': f'{_("Companies")} - {role.name}'}
    queryset = baseClass.objects.filter(role=id)
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    context['tags1'] = roles_tags()
    return myrender(request, context)
