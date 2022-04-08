from django import forms
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Company, Account
from Baumanagement.models.models_contracts import Payment, Contract
from Baumanagement.models.models_projects import Project
from Baumanagement.tables.tables_payments import PaymentTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, \
    generate_next_objects_table

baseClass = Payment
tableClass = PaymentTable


class FormClass(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contract'].queryset = Contract.objects.filter(open=True)

    class Meta:
        model = baseClass
        fields = baseClass.form_fields
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}


def objects_table(request):
    context = {}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    context = {'tables': []}
    queryset = baseClass.objects.filter(id=id)
    payment = queryset.first()

    context['breadcrumbs'] = [{'link': reverse(baseClass.url), 'text': _("All")},
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


def company_payments(request, id):
    company = Company.objects.get(id=id)
    context = {}
    queryset = baseClass.objects.filter(Q(account_from__company=company) | Q(account_to__company=company))

    context['breadcrumbs'] = [{'link': reverse(baseClass.url), 'text': _("All")},
                              {'text': company.name}]

    form = FormClass()
    form.fields["contract"].queryset = Contract.objects.filter(company=company, open=True)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def project_payments(request, id):
    project = Project.objects.get(id=id)
    context = {}
    queryset = baseClass.objects.filter(contract__project=project)

    context['breadcrumbs'] = [{'link': reverse(baseClass.url), 'text': _("All")},
                              {'link': reverse('company_id_payments', args=[project.company.id]),
                               'text': project.company.name},
                              {'text': project.name}]

    form = FormClass()
    form.fields["contract"].queryset = Contract.objects.filter(project=project, open=True)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def contract_payments(request, id):
    contract = Contract.objects.get(id=id)
    context = {}
    queryset = baseClass.objects.filter(contract=contract)

    context['breadcrumbs'] = [{'link': reverse(baseClass.url), 'text': _("All")},
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


def accounts_querysets(form, contract):
    accounts_from = Account.objects.filter(company=contract.project.company, currency=contract.currency, open=True)
    accounts_to = Account.objects.filter(company=contract.company, currency=contract.currency, open=True)
    form.fields['account_from'].queryset = accounts_from if contract.type == Contract.BUY else accounts_to
    form.fields['account_to'].queryset = accounts_to if contract.type == Contract.BUY else accounts_from
    return accounts_from, accounts_to


def generate_payments_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)
