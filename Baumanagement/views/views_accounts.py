from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Account, Company, Currency
from Baumanagement.tables.tables_accounts import AccountTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, \
    generate_next_objects_table
from Baumanagement.views.views_payments import generate_payments_by_queryset, account_payments_qs

baseClass = Account
tableClass = AccountTable


class FormClass(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(open=True)
        self.fields['currency'].queryset = Currency.objects.filter(open=True)
        self.fields['currency'].initial = Currency.objects.get(code='EUR')

    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = {}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    context = {'tables': []}
    queryset = baseClass.objects.filter(id=id)
    account = queryset.first()

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id_accounts', args=[account.company.id]),
                               'text': account.company.name},
                              {'text': account.name}]

    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)

    payments = account_payments_qs(account)
    generate_payments_by_queryset(request, context, payments)

    return myrender(request, context)


def company_accounts(request, id):
    company = Company.objects.get(id=id)
    context = {}
    queryset = company.accounts.all()

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': company.name}]

    form = FormClass()
    form.fields["company"].initial = company
    form.fields['company'].queryset = Company.objects.filter(id=id)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def generate_accounts_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)
