from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from bank_accounts.views import generate_accounts_by_queryset
from bills.views import company_bills_qs, generate_bills_by_queryset
from companies.models import Company
from companies.models_labels import CompanyLabel
from companies.tables import CompanyTable
from contacts.views import generate_contacts_by_queryset
from contracts.models import Contract
from contracts.views import company_contracts_qs, generate_contracts_by_queryset
from main.views import get_base_context, generate_objects_table, myrender, generate_object_table, \
    generate_next_objects_table, labels
from payments.views import company_payments_qs, generate_payments_by_queryset
from projects.views import generate_projects_by_queryset

baseClass = Company
tableClass = CompanyTable
labelClass = CompanyLabel


class FormClass(forms.ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


@login_required
def objects_table(request):
    context = get_base_context(request)
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    context['labels'] = labels(labelClass)
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
