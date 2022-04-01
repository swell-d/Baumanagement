from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Project
from Baumanagement.tables.tables_projects import ProjectTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, \
    generate_next_objects_table
from Baumanagement.views.views_contracts import generate_contracts_by_queryset

baseClass = Project
tableClass = ProjectTable


class FormClass(ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = {}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    queryset = baseClass.objects.filter(id=id)
    context = {'titel1': f'{_("Project")} - {queryset.first().name}', 'tables': []}
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    contracts = queryset.first().contracts.all()
    generate_contracts_by_queryset(request, context, contracts)
    return myrender(request, context)


def generate_projects_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)
