from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import CompanyRole, Company
from Baumanagement.models.models_contracts import Contract
from Baumanagement.tables.tables_companies import CompanyTable
from main.views import myrender, generate_objects_table, generate_object_table, generate_next_objects_table, \
    get_base_context
from Baumanagement.views.views_accounts import generate_accounts_by_queryset
from Baumanagement.views.views_bills import generate_bills_by_queryset, company_bills_qs
from Baumanagement.views.views_contacts import generate_contacts_by_queryset
from Baumanagement.views.views_contracts import generate_contracts_by_queryset, company_contracts_qs
from Baumanagement.views.views_payments import generate_payments_by_queryset, company_payments_qs
from Baumanagement.views.views_projects import generate_projects_by_queryset

baseClass = Company
tableClass = CompanyTable


class FormClass(forms.ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def tags():
    html = f'''<a href="{reverse('companies')}">{_('All')}</a> ({baseClass.objects.count()}), '''
    html += ', '.join(
        f'''#<a href="{reverse('companies_id', args=[role.id])}">{role.name}</a> ({role.count})'''
        for role in CompanyRole.objects.order_by('name') if role.count > 0)
    html += ' &#9881;<a href="' + reverse('companyroles') + '">' + _('Manage roles') + '</a>'
    return format_html(html)


@login_required
def objects_table(request):
    context = get_base_context(request)
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    context['tags1'] = tags()
    return myrender(request, context)


@login_required
def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)
    if queryset.first() is None:
        raise Http404
    company = queryset.first()

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': company.name}]

    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)

    accounts = company.accounts.all()
    generate_accounts_by_queryset(request, context, accounts)

    contacts = company.contacts.all()
    generate_contacts_by_queryset(request, context, contacts)

    projects = company.projects.all()
    generate_projects_by_queryset(request, context, projects)

    contracts = company_contracts_qs(company)
    generate_contracts_by_queryset(request, context, contracts)

    bills = company_bills_qs(company)
    generate_bills_by_queryset(request, context, bills)

    payments = company_payments_qs(company)
    generate_payments_by_queryset(request, context, payments)

    partners = get_partners(company, contracts)
    generate_next_objects_table(request, context, baseClass, tableClass, partners, _('Partners'))

    return myrender(request, context)


@login_required
def company_companies(request, id):
    context = get_base_context(request)
    company = get_object_or_404(Company, id=id)

    contracts = Contract.objects.filter(Q(project__company=company) | Q(company=company))
    queryset = get_partners(company, contracts)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id', args=[company.id]), 'text': company.name},
                              {'text': _('Partners')}]

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def get_partners(company, contracts):
    partners_ids = set()
    for each in contracts:
        partners_ids.add(each.company.id)
        partners_ids.add(each.project.company.id)
    partners_ids.discard(company.id)
    return Company.objects.filter(id__in=partners_ids)


@login_required
def companies_by_role(request, id):
    context = get_base_context(request)
    role = get_object_or_404(CompanyRole, id=id)
    queryset = baseClass.objects.filter(role=id)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': role.name}]

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    context['tags1'] = tags()
    return myrender(request, context)
