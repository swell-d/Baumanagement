from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import CompanyRole
from Baumanagement.tables.tables import MyTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, get_base_context, my404

baseClass = CompanyRole


class TableClass(MyTable):
    class Meta(MyTable.Meta):
        model = baseClass
        fields = baseClass.table_fields


class FormClass(forms.ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = get_base_context(request)
    generate_objects_table(request, context, baseClass, TableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)
    if queryset.first() is None:
        return my404(request, None)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': queryset.first().name}]

    generate_object_table(request, context, baseClass, TableClass, FormClass, queryset)
    return myrender(request, context)
