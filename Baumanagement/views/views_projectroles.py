from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_projects import ProjectRole
from Baumanagement.tables.tables_projectroles import ProjectRoleTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table

baseClass = ProjectRole
tableClass = ProjectRoleTable


class FormClass(forms.ModelForm):
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

    context['breadcrumbs'] = [{'link': reverse(baseClass.url), 'text': _("All")},
                              {'text': queryset.first().name}]

    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)
