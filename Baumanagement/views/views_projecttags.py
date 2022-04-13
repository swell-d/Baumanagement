from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_projects import ProjectTag
from Baumanagement.tables.tables import MyTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table

baseClass = ProjectTag


class TableClass(MyTable):
    class Meta(MyTable.Meta):
        model = baseClass
        fields = baseClass.table_fields


class FormClass(forms.ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = {}
    context['nodes'] = ProjectTag.objects.filter(parent__isnull=True)
    context['nodes_link'] = 'projecttag'
    generate_objects_table(request, context, baseClass, TableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    context = {'tables': []}
    queryset = baseClass.objects.filter(id=id)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': queryset.first().name}]

    generate_object_table(request, context, baseClass, TableClass, FormClass, queryset)
    return myrender(request, context)
