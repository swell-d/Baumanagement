from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from bank_accounts.models import Account
from bank_accounts.tables import AccountTable
from companies.models import Company
from currencies.models import Currency
from main.view_functions import get_base_context
from main.view_renders import myrender
from main.views import generate_objects_table, generate_object_table, \
    generate_next_objects_table
from payments.views import account_payments_qs, generate_payments_by_queryset

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


@login_required
def objects_table(request):
    context = get_base_context(request)
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


@login_required
def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)
    if queryset.first() is None:
        raise Http404
    account = queryset.first()

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id_accounts', args=[account.company.id]),
                               'text': account.company.name},
                              {'text': account.name}]

    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)

    payments = account_payments_qs(account)
    generate_payments_by_queryset(request, context, payments)

    return myrender(request, context)


@login_required
def company_accounts(request, id):
    context = get_base_context(request)
    company = get_object_or_404(Company, id=id)
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
