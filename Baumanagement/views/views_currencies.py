from django.forms import ModelForm

from Baumanagement.models.models_company import Currency
from Baumanagement.tables.tables_currencies import CurrencyTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table

baseClass = Currency
tableClass = CurrencyTable


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