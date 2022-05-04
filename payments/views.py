from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Case, When
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from bank_accounts.models import Account
from bills.views import qs_annotate
from companies.models import Company
from contracts.models import Contract
from main.views import get_base_context, generate_objects_table, myrender, generate_object_table, \
    generate_next_objects_table, labels
from payments.models import Payment
from payments.models_labels import PaymentLabel
from payments.tables import PaymentTable
from projects.models import Project

baseClass = Payment
tableClass = PaymentTable
labelClass = PaymentLabel


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
    context['labels'] = labels(labelClass)
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
    payment = queryset.first()

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id_payments', args=[payment.contract.project.company.id]),
                               'text': payment.contract.project.company.name},
                              {'link': reverse('project_id_payments', args=[payment.contract.project.id]),
                               'text': payment.contract.project.name},
                              {'link': reverse('contract_id_payments', args=[payment.contract.id]),
                               'text': payment.contract.name},
                              {'text': payment.name}]

    form = FormClass(instance=payment)
    accounts_querysets(form, payment.contract)
    context['form'] = form

    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


@login_required
def company_payments(request, id):
    context = get_base_context(request)
    context['labels'] = labels(labelClass)
    company = get_object_or_404(Company, id=id)
    queryset = company_payments_qs(company)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': company.name}]

    form = FormClass()
    form.fields["contract"].queryset = Contract.objects.filter(company=company, open=True)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def company_payments_qs(company):
    return baseClass.objects.filter(Q(account_from__company=company) | Q(account_to__company=company)).annotate(
        amount_netto=Case(When(account_from__company=company, then=-F('amount_netto_positiv')),
                          When(account_to__company=company, then='amount_netto_positiv'))).annotate(
        amount_brutto=Case(When(account_from__company=company, then=-F('amount_brutto_positiv')),
                           When(account_to__company=company, then='amount_brutto_positiv')))


@login_required
def account_payments(request, id):
    context = get_base_context(request)
    context['labels'] = labels(labelClass)
    account = get_object_or_404(Account, id=id)
    queryset = account_payments_qs(account)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id', args=[account.company.id]), 'text': account.company.name},
                              {'text': account.name}]

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def account_payments_qs(account):
    return baseClass.objects.filter(Q(account_from=account) | Q(account_to=account)).annotate(
        amount_netto=Case(When(account_from=account, then=-F('amount_netto_positiv')),
                          When(account_to=account, then='amount_netto_positiv'))).annotate(
        amount_brutto=Case(When(account_from=account, then=-F('amount_brutto_positiv')),
                           When(account_to=account, then='amount_brutto_positiv')))


@login_required
def project_payments(request, id):
    context = get_base_context(request)
    context['labels'] = labels(labelClass)
    project = get_object_or_404(Project, id=id)
    queryset = project_payments_qs(project)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id_payments', args=[project.company.id]),
                               'text': project.company.name},
                              {'text': project.name}]

    form = FormClass()
    form.fields["contract"].queryset = Contract.objects.filter(project=project, open=True)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def project_payments_qs(project):
    return qs_annotate(baseClass.objects.filter(contract__project=project))


@login_required
def contract_payments(request, id):
    context = get_base_context(request)
    context['labels'] = labels(labelClass)
    contract = get_object_or_404(Contract, id=id)
    queryset = contract_payments_qs(contract)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id_payments', args=[contract.project.company.id]),
                               'text': contract.project.company.name},
                              {'link': reverse('project_id_payments', args=[contract.project.id]),
                               'text': contract.project.name},
                              {'text': contract.name}]

    form = FormClass()
    form.fields['contract'].queryset = Contract.objects.filter(id=id)
    form.fields["contract"].initial = contract

    accounts_from, accounts_to = accounts_querysets(form, contract)
    form.fields[
        "account_from"].initial = accounts_from.last() if contract.type == Contract.BUY else accounts_to.last()
    form.fields[
        "account_to"].initial = accounts_to.last() if contract.type == Contract.BUY else accounts_from.last()

    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def contract_payments_qs(contract):
    return qs_annotate(baseClass.objects.filter(contract=contract))


def accounts_querysets(form, contract):
    accounts_from = Account.objects.filter(company=contract.project.company, currency=contract.currency, open=True)
    accounts_to = Account.objects.filter(company=contract.company, currency=contract.currency, open=True)
    form.fields['account_from'].queryset = accounts_from if contract.type == Contract.BUY else accounts_to
    form.fields['account_to'].queryset = accounts_to if contract.type == Contract.BUY else accounts_from
    return accounts_from, accounts_to


def generate_payments_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)
