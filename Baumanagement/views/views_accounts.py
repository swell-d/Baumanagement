from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Account
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
    context = {'titel1': _('All accounts')}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    queryset = baseClass.objects.filter(id=id)
    context = {'titel1': f'{_("Account")} - {queryset.first().name}', 'tables': []}
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def generate_accounts_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)
