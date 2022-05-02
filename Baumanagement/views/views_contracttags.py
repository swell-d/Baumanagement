from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_contracts import ContractTag
from Baumanagement.tables.tables import MyTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, get_base_context

baseClass = ContractTag


class TableClass(MyTable):
    class Meta(MyTable.Meta):
        model = baseClass
        fields = baseClass.table_fields


class FormClass(forms.ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


@login_required
def objects_table(request):
    context = get_base_context(request)
    context['nodes'] = ContractTag.objects.filter(parent__isnull=True)
    context['nodes_link'] = 'contracttag'
    generate_objects_table(request, context, baseClass, TableClass, FormClass)
    return myrender(request, context)


@login_required
def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)
    if queryset.first() is None:
        raise Http404

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': queryset.first().name}]

    generate_object_table(request, context, baseClass, TableClass, FormClass, queryset)
    return myrender(request, context)
