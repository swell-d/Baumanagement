from decimal import Decimal

from bills.tables import BillTable
from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Case, When
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Company
from Baumanagement.models.models_projects import Project
from bills.models import Bill
from contracts.models import Contract
from main.views import get_base_context, generate_objects_table, myrender, generate_object_table, \
    generate_next_objects_table

baseClass = Bill
tableClass = BillTable


class FormClass(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contract'].queryset = Contract.objects.filter(open=True)

    class Meta:
        model = baseClass
        fields = baseClass.form_fields
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}


@login_required
def objects_table(request):
    context = get_base_context(request)
    queryset = qs_annotate(baseClass.objects)
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


@login_required
def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)
    if queryset.first() is None:
        raise Http404
    queryset = queryset.annotate(amount_netto=F('amount_netto_positiv'),
                                 amount_brutto=F('amount_brutto_positiv'))
    bill = queryset.first()

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id_bills', args=[bill.contract.project.company.id]),
                               'text': bill.contract.project.company.name},
                              {'link': reverse('project_id_bills', args=[bill.contract.project.id]),
                               'text': bill.contract.project.name},
                              {'link': reverse('contract_id_bills', args=[bill.contract.id]),
                               'text': bill.contract.name},
                              {'text': bill.name}]

    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    if 'buttons' in context:
        context['buttons'].append('Print')
    return myrender(request, context)


@login_required
def company_bills(request, id):
    context = get_base_context(request)
    company = get_object_or_404(Company, id=id)
    queryset = company_bills_qs(company)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': company.name}]

    form = FormClass()
    form.fields["contract"].queryset = Contract.objects.filter(company=company, open=True)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def company_bills_qs(company):
    return baseClass.objects.filter(
        Q(contract__project__company=company, contract__type=Contract.SELL) |
        Q(contract__company=company, contract__type=Contract.BUY)).annotate(
        amount_netto=F('amount_netto_positiv'),
        amount_brutto=F('amount_brutto_positiv'))


@login_required
def project_bills(request, id):
    context = get_base_context(request)
    project = get_object_or_404(Project, id=id)
    queryset = project_bills_qs(project)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id_bills', args=[project.company.id]),
                               'text': project.company.name},
                              {'text': project.name}]

    form = FormClass()
    form.fields["contract"].queryset = Contract.objects.filter(project=project, open=True)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def project_bills_qs(project):
    return qs_annotate(baseClass.objects.filter(contract__project=project))


@login_required
def contract_bills(request, id):
    context = get_base_context(request)
    contract = get_object_or_404(Contract, id=id)
    queryset = contract_bills_qs(contract)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id_bills', args=[contract.project.company.id]),
                               'text': contract.project.company.name},
                              {'link': reverse('project_id_bills', args=[contract.project.id]),
                               'text': contract.project.name},
                              {'text': contract.name}]

    form = FormClass()
    form.fields["contract"].initial = contract
    form.fields['contract'].queryset = Contract.objects.filter(id=id)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def contract_bills_qs(contract):
    return qs_annotate(baseClass.objects.filter(contract=contract))


def generate_bills_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)


def qs_annotate(queryset):
    return queryset.annotate(
        amount_netto=Case(When(contract__type=Contract.BUY, then=-F('amount_netto_positiv')),
                          When(contract__type=Contract.SELL, then='amount_netto_positiv'),
                          default=Decimal(0))).annotate(
        amount_brutto=Case(When(contract__type=Contract.BUY, then=-F('amount_brutto_positiv')),
                           When(contract__type=Contract.SELL, then='amount_brutto_positiv'),
                           default=Decimal(0)))
