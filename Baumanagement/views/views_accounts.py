from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Account, Company
from Baumanagement.tables.tables_accounts import AccountTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, \
    generate_next_objects_table

baseClass = Account
tableClass = AccountTable


class FormClass(ModelForm):
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
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def company_accounts(request, id):
    company = Company.objects.get(id=id)
    context = {'titel1': f'{_("Company")} "{company.name}" - {_("Accounts")}'}
    queryset = company.accounts.all()
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def generate_accounts_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)
