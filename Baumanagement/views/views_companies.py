from django import forms
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Bill, Payment, Contract
from Baumanagement.models.models_company import CompanyRole, Company
from Baumanagement.tables.tables_companies import CompanyTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, \
    generate_next_objects_table
from Baumanagement.views.views_accounts import generate_accounts_by_queryset
from Baumanagement.views.views_bills import generate_bills_by_queryset
from Baumanagement.views.views_contacts import generate_contacts_by_queryset
from Baumanagement.views.views_contracts import generate_contracts_by_queryset
from Baumanagement.views.views_payments import generate_payments_by_queryset
from Baumanagement.views.views_projects import generate_projects_by_queryset

baseClass = Company
tableClass = CompanyTable


class FormClass(forms.ModelForm):
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
    company = queryset.first()

    context['breadcrumbs'] = [{'link': reverse(baseClass.url), 'text': _("All")},
                              {'text': company.name}]

    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)

    accounts = company.accounts.all()
    generate_accounts_by_queryset(request, context, accounts)

    contacts = company.contacts.all()
    generate_contacts_by_queryset(request, context, contacts)

    projects = company.projects.all()
    generate_projects_by_queryset(request, context, projects)

    contracts = Contract.objects.filter(Q(project__company=company) | Q(company=company))
    generate_contracts_by_queryset(request, context, contracts)

    bills = Bill.objects.filter(
        Q(contract__project__company=company, contract__type=Contract.SELL) |
        Q(contract__company=company, contract__type=Contract.BUY))
    generate_bills_by_queryset(request, context, bills)

    payments = Payment.objects.filter(Q(account_from__company=company) | Q(account_to__company=company))
    generate_payments_by_queryset(request, context, payments)

    partners_ids = set()
    for each in contracts:
        partners_ids.add(each.company.id)
        partners_ids.add(each.project.company.id)
    partners_ids.discard(company.id)
    partners = Company.objects.filter(id__in=partners_ids)
    generate_next_objects_table(request, context, baseClass, tableClass, partners, _('Partners'))

    return myrender(request, context)


def companies_by_role(request, id):
    role = CompanyRole.objects.get(id=id)
    context = {}
    queryset = baseClass.objects.filter(role=id)

    context['breadcrumbs'] = [{'link': reverse(baseClass.url), 'text': _("All")},
                              {'text': role.name}]

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    context['tags1'] = roles_tags()
    return myrender(request, context)
